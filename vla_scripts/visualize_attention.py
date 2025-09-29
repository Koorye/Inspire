"""
This script extracts attention maps from a VLA model for a given task and visualizes them.
To acquire the direct attention maps between image patches and the action token, it merges 
intermediate tokens and decomposes the attention matrix.
"""

import os
os.environ['PRISMATIC_DATA_ROOT'] = ''
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import sys
sys.path.append('..')

import tensorflow as tf
tf.config.list_physical_devices('GPU')

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from PIL import Image
from pathlib import Path
from tqdm import tqdm

from experiments.robot.openvla_utils import apply_center_crop
from experiments.robot.robot_utils import get_model
from vla_scripts.openvla_with_vqa import OpenVLAWithVQA


def get_minivla():
    class GenerateConfig:
        model_family = "prismatic"                    # Model family
        hf_token = Path(".hf_token")                       # Model family
        pretrained_checkpoint = "/your/ckpt/path/here"     # Pretrained checkpoint path
        load_in_8bit = False                       # (For OpenVLA only) Load with 8-bit quantization
        load_in_4bit = False                       # (For OpenVLA only) Load with 4-bit quantization

        center_crop = True                         # Center crop? (if trained w/ random crop image aug)
        obs_history = 1                             # Number of images to pass in from history
        use_wrist_image = False                    # Use wrist images (doubles the number of input images)

        task_suite_name: str = "libero_90"          # Task suite.
        num_steps_wait: int = 10                         # Number of steps to wait for objects to stabilize in sim
        num_trials_per_task: int = 50                    # Number of rollouts per task
        image_sequence_len = 1

    cfg = GenerateConfig()
    model = get_model(cfg)
    model.eval()
    return cfg, model


def get_minivla_vqa():
    class GenerateConfig:
        model_family = "prismatic"                    # Model family
        hf_token = Path(".hf_token")                       # Model family
        pretrained_checkpoint = "/your/ckpt/path/here"     # Pretrained checkpoint path
        load_in_8bit = False                       # (For OpenVLA only) Load with 8-bit quantization
        load_in_4bit = False                       # (For OpenVLA only) Load with 4-bit quantization

        center_crop = True                         # Center crop? (if trained w/ random crop image aug)
        obs_history = 1                             # Number of images to pass in from history
        use_wrist_image = False                    # Use wrist images (doubles the number of input images)

        task_suite_name: str = "libero_90"          # Task suite.
        num_steps_wait: int = 10                         # Number of steps to wait for objects to stabilize in sim
        num_trials_per_task: int = 50                    # Number of rollouts per task
        image_sequence_len = 1
        
        mode = 'coarse_direction'
        check_catch = True
        check_close = False

    cfg = GenerateConfig()
    model = OpenVLAWithVQA(get_model(cfg), mode=cfg.mode, check_catch=cfg.check_catch, check_close=cfg.check_close)
    model.vla.eval()
    return cfg, model


def get_prismatic_vla_features(vla, processor, base_vla_name, obs, task_label, unnorm_key, center_crop=False, **kwargs):
    """ Get features from the VLA model. """

    if not isinstance(obs["full_image"], list):
        obs["full_image"] = [obs["full_image"]]

    processed_images = []

    for img in obs["full_image"]:
        image = Image.fromarray(img)
        image = image.convert("RGB")

        if center_crop:
            temp_image = np.array(image)  # (H, W, C)
            crop_scale = 0.9
            sqrt_crop_scale = math.sqrt(crop_scale)
            temp_image_cropped = apply_center_crop(
                temp_image,
                t_h=int(sqrt_crop_scale * temp_image.shape[0]),
                t_w=int(sqrt_crop_scale * temp_image.shape[1]),
            )
            temp_image = Image.fromarray(temp_image_cropped)
            temp_image = temp_image.resize(
                image.size, Image.Resampling.BILINEAR
            )  # IMPORTANT: dlimp uses BILINEAR resize
            image = temp_image

        processed_images.append(image)

    if len(processed_images) == 1:
        processed_images = processed_images[0]

    return vla.predict_features(processed_images, task_label, unnorm_key=unnorm_key, **kwargs)


@torch.no_grad()
def get_attention(cfg, model, image, task_description):
    """ Get attention map for the given image and task description. """

    observation = {'full_image': [np.array(image)]}
    output = get_prismatic_vla_features(model, None, None, observation, task_description, cfg.task_suite_name, 
                                        cfg.center_crop, use_cache=False, return_dict_in_generate=True, output_hidden_states=True, output_attentions=True)
    attention = output['attentions'][-1][-1][0].mean(0)
    return attention.detach().float().cpu().numpy()


@torch.no_grad()
def get_attention_vqa(cfg, model, image, task_description):
    """ Get attention map for the given image and task description for InSpire. """

    observation = {'full_image': [np.array(image)]}
    output = get_prismatic_vla_features(model, None, None, observation, task_description, cfg.task_suite_name, 
                                        cfg.center_crop, use_cache=False)
    attention = output['attentions'][-1][-1][0].mean(0)
    return attention.detach().float().cpu().numpy()


def gif_to_images(gif_path):
    """ Convert a GIF file to a list of PIL images. """

    gif = Image.open(gif_path)
    gif.seek(0)
    images = []
    while True:
        try:
            images.append(gif.copy())
            gif.seek(gif.tell() + 1)
        except EOFError:
            break
    return images


def image_to_patches(image, patch_size):
    """ Convert an image to a list of patches. Each patch is represented by a string like '<|p0,0|>'. """

    patches = []
    for i in range(0, image.size[0], patch_size):
        for j in range(0, image.size[1], patch_size):
            patches.append(f'<|p{i},{j}|>')
    return patches


def get_final_attention(model, attention, image, patch_size, task_description):
    """ Get the final attention matrix and save it to a CSV file. """

    patches = image_to_patches(image, patch_size)

    prompt_builder = model.get_prompt_builder()
    prompt_builder.add_turn(role="human", message=f"What action should the robot take to {task_description.lower()}?")
    prompt_text = prompt_builder.get_prompt()
    texts = model.llm_backbone.tokenizer.tokenize(prompt_text)
    texts = [t.replace('Ġ', '').replace('Ċ', '') for t in texts]
    assert len(attention) == len(patches) + len(texts) + 7 - 1

    labels = patches + texts[1:] + ['x', 'y', 'z', 'pitch', 'yaw', 'roll', 'grip']
    df = pd.DataFrame(attention, index=labels, columns=labels)
    df.to_csv('attention.csv', index=True, header=True)
    return pd.read_csv('attention.csv', index_col=0)


def get_final_attention_vqa(model, attention, image, patch_size, task_description):
    """ Get the final attention matrix and save it to a CSV file for InSpire. """

    patches = image_to_patches(image, patch_size)

    prompt_text = model.prompt_builder.get_prompt()
    texts = model.vla.llm_backbone.tokenizer.tokenize(prompt_text)
    texts = [t.replace('Ġ', '').replace('Ċ', '') for t in texts]
    assert len(attention) == len(patches) + len(texts) + 7 - 1

    labels = patches + texts[1:] + ['x', 'y', 'z', 'pitch', 'yaw', 'roll', 'grip']
    df = pd.DataFrame(attention, index=labels, columns=labels)
    df.to_csv('attention.csv', index=True, header=True)
    return pd.read_csv('attention.csv', index_col=0)


def patch_id_to_image(patch_id, patch_size, origin_image, resize_size=None):
    """ Convert a patch ID like '<|p0,0|>' to a PIL image patch. """

    # patch_id like '<|p0,0|>'
    # get the coordinates
    coords = patch_id[3:-2].split(',')
    x = int(coords[0])
    y = int(coords[1])
    # get the patch
    patch = origin_image.crop((x, y, x + patch_size, y + patch_size))
    if resize_size is not None:
        patch = patch.resize((resize_size, resize_size), Image.Resampling.BILINEAR)
    return patch


def tile_images(images, cols=5):
    """ Tile a list of PIL images into a single image. """

    rows = math.ceil(len(images) / cols)
    tile_width = images[0].size[0]
    tile_height = images[0].size[1]
    tiled_image = Image.new('RGB', (tile_width * cols, tile_height * rows))
    for i, image in enumerate(images):
        x = (i % cols) * tile_width
        y = (i // cols) * tile_height
        tiled_image.paste(image, (x, y))
    return tiled_image


def merge_tokens(df):
    """ 
    Merge tokens in the attention matrix based on specific patterns. 
    This function will merge serveral tokens into one token,
    resulting in an attention matrix that only contains image patch tokens, system token, and the action token.
    """

    def merge_indices(mat, indices):
        # sum the rows and columns of the matrix
        indices = sorted(indices)
        mat[indices[0]] = mat[indices].sum(axis=0)
        mat[:, indices[0]] = mat[:, indices].sum(axis=1)
        mat = np.delete(mat, indices[1:], axis=0)
        mat = np.delete(mat, indices[1:], axis=1)
        return mat
    
    def remove_indices(mat, indices):
        # remove the rows and columns of the matrix
        indices = sorted(indices)
        mat = np.delete(mat, indices, axis=0)
        mat = np.delete(mat, indices, axis=1)
        return mat

    columns = df.columns.tolist()
    attn = df.values
    
    unnamed_indices = [i for i, col in enumerate(columns) if 'unnamed' in col.lower()]
    columns = [col for i, col in enumerate(columns) if i not in unnamed_indices]
    attn = remove_indices(attn, unnamed_indices)

    action_start = columns.index('<|im_start|>.1')
    action_end = columns.index('grip')
    action_indices = range(action_start, action_end + 1)
    attn = merge_indices(attn, action_indices)
    columns = columns[:action_start] + ['action'] + columns[action_end + 1:]

    insturction_start = columns.index('<|im_start|>')
    insturction_end = columns.index('<|im_end|>.1')
    instruction_indices = range(insturction_start, insturction_end + 1)
    attn = merge_indices(attn, instruction_indices)
    columns = columns[:insturction_start] + ['instruction'] + columns[insturction_end + 1:]
    
    system_start = columns.index('system')
    system_end = columns.index('<|im_end|>')
    system_indices = range(system_start, system_end + 1)
    attn = merge_indices(attn, system_indices)
    columns = columns[:system_start] + ['system'] + columns[system_end + 1:]
    
    return pd.DataFrame(attn, index=columns, columns=columns)  


def merge_tokens_vqa(df):
    """ 
    Merge tokens in the attention matrix based on specific patterns for InSpire.
    This function will merge serveral tokens into one token,
    resulting in an attention matrix that only contains image patch tokens, system token, 
    merged InSpire tokens (each token contains all tokens from each question + answer), and the action token.
    """

    def merge_indices(mat, indices):
        # sum the rows and columns of the matrix
        indices = sorted(indices)
        mat[indices[0]] = mat[indices].sum(axis=0)
        mat[:, indices[0]] = mat[:, indices].sum(axis=1)
        mat = np.delete(mat, indices[1:], axis=0)
        mat = np.delete(mat, indices[1:], axis=1)
        return mat
    
    def remove_indices(mat, indices):
        # remove the rows and columns of the matrix
        indices = sorted(indices)
        mat = np.delete(mat, indices, axis=0)
        mat = np.delete(mat, indices, axis=1)
        return mat

    columns = df.columns.tolist()
    attn = df.values
    
    unnamed_indices = [i for i, col in enumerate(columns) if 'unnamed' in col.lower()]
    columns = [col for i, col in enumerate(columns) if i not in unnamed_indices]
    attn = remove_indices(attn, unnamed_indices)

    if '<|im_start|>.5' in columns:
        action_start = columns.index('<|im_start|>.5')
        action_end = columns.index('grip')
        action_indices = range(action_start, action_end + 1)
        attn = merge_indices(attn, action_indices)
        columns = columns[:action_start] + ['action'] + columns[action_end + 1:]

        insturction_start = columns.index('<|im_start|>.4')
        insturction_end = columns.index('<|im_end|>.5')
        instruction_indices = range(insturction_start, insturction_end + 1)
        attn = merge_indices(attn, instruction_indices)
        columns = columns[:insturction_start] + ['instruction'] + columns[insturction_end + 1:]

        obj2_start = columns.index('<|im_start|>.2')
        obj2_end = columns.index('<|im_end|>.4')
        obj2_indices = range(obj2_start, obj2_end + 1)
        attn = merge_indices(attn, obj2_indices)
        columns = columns[:obj2_start] + ['obj2'] + columns[obj2_end + 1:]
        
        obj1_start = columns.index('<|im_start|>')
        obj1_end = columns.index('<|im_end|>.2')
        obj1_indices = range(obj1_start, obj1_end + 1)
        attn = merge_indices(attn, obj1_indices)
        columns = columns[:obj1_start] + ['obj1'] + columns[obj1_end + 1:]

        system_start = columns.index('system')
        system_end = columns.index('<|im_end|>')
        system_indices = range(system_start, system_end + 1)
        attn = merge_indices(attn, system_indices)
        columns = columns[:system_start] + ['system'] + columns[system_end + 1:]
    else:
        action_start = columns.index('<|im_start|>.3')
        action_end = columns.index('grip')
        action_indices = range(action_start, action_end + 1)
        attn = merge_indices(attn, action_indices)
        columns = columns[:action_start] + ['action'] + columns[action_end + 1:]

        insturction_start = columns.index('<|im_start|>.2')
        insturction_end = columns.index('<|im_end|>.3')
        instruction_indices = range(insturction_start, insturction_end + 1)
        attn = merge_indices(attn, instruction_indices)
        columns = columns[:insturction_start] + ['instruction'] + columns[insturction_end + 1:]
        
        obj1_start = columns.index('<|im_start|>')
        obj1_end = columns.index('<|im_end|>.2')
        obj1_indices = range(obj1_start, obj1_end + 1)
        attn = merge_indices(attn, obj1_indices)
        columns = columns[:obj1_start] + ['obj1'] + columns[obj1_end + 1:]

        system_start = columns.index('system')
        system_end = columns.index('<|im_end|>')
        system_indices = range(system_start, system_end + 1)
        attn = merge_indices(attn, system_indices)
        columns = columns[:system_start] + ['system'] + columns[system_end + 1:]
    
    return pd.DataFrame(attn, index=columns, columns=columns)  


def decompose_tokens(df):
    """
    Merge tokens in the attention matrix based on specific patterns.
    The function will merge all intermediate tokens' attention weights into the final action token,
    resulting in an attention matrix that only contains image patch tokens and the action token.
    """

    def decompose_indice(mat, columns, indice):
        """
        This function takes a matrix and a column index, and merges the attention weights of the token
        at the given index with the next token, then removes the token at the given index.

        Example:
        mat:
        [[ 0.1, 0.2, 0.3] 
        [ 0.4, 0.5, 0.6]
        [ 0.7, 0.8, 0.9]]
        columns: ['A', 'B', 'C']
        indice: 1

        After decomposition, mat becomes:
        [[0.1  0.3 ]
        [1.02 1.38]]
        columns: ['A', 'C']
        """

        weights_this_to_other = mat[indice]
        weight_next_to_this = mat[indice + 1, indice]
        weights = weights_this_to_other * weight_next_to_this
        mat[indice + 1] += weights
        mat = np.delete(mat, indice, axis=0)
        mat = np.delete(mat, indice, axis=1)
        columns = columns[:indice] + columns[indice + 1:]
        return mat, columns
    
    columns = df.columns.tolist()
    attn = df.values

    while '<|p' not in columns[len(attn) - 2]:
        attn, columns = decompose_indice(attn, columns, len(attn) - 2)
    
    return pd.DataFrame(attn, index=columns, columns=columns)
    

def matrix_to_triples(df, thresh=0.1):
    """ Convert the attention matrix to a list of triples (source, target, weight). """

    columns = df.columns
    attn = df.values
    triples = []
    for i in range(len(columns)):
        for j in range(len(columns)):
            if '<|p' in columns[i] and '<|p' in columns[j]:
                continue
            if i > j and attn[i][j] > thresh:
                triples.append((columns[i], columns[j], attn[i][j]))
    return pd.DataFrame(triples, columns=['source', 'target', 'weight'])


def value_to_rgb(value):
    """ Coolwarm color map for value in [0, 255] """

    if value < 0 or value > 255:
        return 0, 0, 0
    # 0~31
    if value >= 0 and value <= 31:
        r = 0
        g = 0
        b = 128 + 4 * (value - 0)
        return r, g, b
    # 32
    if value == 32:
        r = 0
        g = 0
        b = 255
        return r, g, b
    # 33~95
    if value >= 33 and value <= 95:
        r = 0
        g = 4 + 4 * (value - 33)
        b = 255
        return r, g, b
    # 96
    if value == 96:
        r = 2
        g = 255
        b = 254
        return r, g, b
    # 97~158
    if value >= 97 and value <= 158:
        r = 6 + 4 * (value - 97)
        g = 255
        b = 250 - 4 * (value - 97)
        return r, g, b
    # 159
    if value == 159:
        r = 254
        g = 255
        b = 1
        return r, g, b
    # 160~223
    if value >= 160 and value <= 223:
        r = 255
        g = 252 - 4 * (value - 160)
        b = 0
        return r, g, b
    # 224~255
    if value >= 224 and value <= 255:
        r = 252 - 4 * (value - 224)
        g = 0
        b = 0
        return r, g, b



gif_root = 'visualization/baseline'
frame_indexs = range(0, 100, 5)
patch_size = 14

cfg, model = get_minivla()

for gif_file in os.listdir(gif_root):
    if not gif_file.endswith('.gif'):
        continue

    gif_path = os.path.join(gif_root, gif_file)
    task_description = gif_file.split('.')[0].split('_')[1]

    images = gif_to_images(gif_path)

    for frame_index in tqdm(frame_indexs):
        if frame_index >= len(images):
            continue
        attention = get_attention(cfg, model, images[frame_index], task_description)
        df = get_final_attention(model, attention, images[frame_index], patch_size, task_description)

        df = merge_tokens(df)
        df = decompose_tokens(df)

        df2 = matrix_to_triples(df, 0.0)
        attn_map = df2['weight'].values.reshape(16, 16)
        attn_map[0, 0] = 0
        plt.imshow(images[frame_index])
        attn_map /= attn_map.max()
        attn_map = Image.fromarray((attn_map * 255).astype(np.uint8)).resize((images[0].size[0], images[0].size[1]), Image.Resampling.BILINEAR)
        
        # r, g, b, alpha
        attn_map_r = np.zeros((attn_map.size[1], attn_map.size[0]), dtype=np.uint8)
        attn_map_g = np.zeros((attn_map.size[1], attn_map.size[0]), dtype=np.uint8)
        attn_map_b = np.zeros((attn_map.size[1], attn_map.size[0]), dtype=np.uint8)
        for i in range(attn_map.size[1]):
            for j in range(attn_map.size[0]):
                value = attn_map.getpixel((j, i))
                r, g, b = value_to_rgb(value)
                attn_map_r[i, j] = r
                attn_map_g[i, j] = g
                attn_map_b[i, j] = b
        
        alpha = np.uint8(np.clip(np.float32(np.array(attn_map)) * 2, 0, 255))
        attn_map = np.stack([attn_map_r, attn_map_g, attn_map_b, alpha], axis=-1)

        plt.imshow(attn_map)
        plt.axis('off')
        os.makedirs(os.path.join(gif_path.split('.')[0]), exist_ok=True)
        plt.savefig(os.path.join(gif_path.split('.')[0], f'{frame_index}_attention_map.png'), bbox_inches='tight', pad_inches=0)
        plt.close()

model.cpu()
del cfg
del model


gif_root = 'visualization/ours'
cfg, model = get_minivla_vqa()

for gif_file in os.listdir(gif_root):
    if not gif_file.endswith('.gif'):
        continue
    
    gif_path = os.path.join(gif_root, gif_file)
    task_description = gif_file.split('.')[0].split('_')[1]

    images = gif_to_images(gif_path)

    for frame_index in tqdm(frame_indexs):
        if frame_index >= len(images):
            continue
        attention = get_attention_vqa(cfg, model, images[frame_index], task_description)
        df = get_final_attention_vqa(model, attention, images[frame_index], patch_size, task_description)

        df = merge_tokens_vqa(df)
        df = decompose_tokens(df)

        df2 = matrix_to_triples(df, 0.0)
        attn_map = df2['weight'].values.reshape(16, 16)
        attn_map[0, 0] = 0
        plt.imshow(images[frame_index])
        attn_map /= attn_map.max()
        attn_map = Image.fromarray((attn_map * 255).astype(np.uint8)).resize((images[0].size[0], images[0].size[1]), Image.Resampling.BILINEAR)
        
        # r, g, b, alpha
        attn_map_r = np.zeros((attn_map.size[1], attn_map.size[0]), dtype=np.uint8)
        attn_map_g = np.zeros((attn_map.size[1], attn_map.size[0]), dtype=np.uint8)
        attn_map_b = np.zeros((attn_map.size[1], attn_map.size[0]), dtype=np.uint8)
        for i in range(attn_map.size[1]):
            for j in range(attn_map.size[0]):
                value = attn_map.getpixel((j, i))
                r, g, b = value_to_rgb(value)
                attn_map_r[i, j] = r
                attn_map_g[i, j] = g
                attn_map_b[i, j] = b
        
        alpha = np.uint8(np.clip(np.float32(np.array(attn_map)) * 2, 0, 255))
        attn_map = np.stack([attn_map_r, attn_map_g, attn_map_b, alpha], axis=-1)

        plt.imshow(attn_map)
        plt.axis('off')
        os.makedirs(os.path.join(gif_path.split('.')[0]), exist_ok=True)
        plt.savefig(os.path.join(gif_path.split('.')[0], f'{frame_index}_attention_map.png'), bbox_inches='tight', pad_inches=0)
        plt.close()
