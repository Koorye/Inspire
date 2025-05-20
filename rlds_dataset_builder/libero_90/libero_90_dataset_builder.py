import os
os.environ['NO_GCE_CHECK'] = 'true'

import tensorflow_datasets as tfds
tfds.core.utils.gcs_utils._is_gcs_disabled = True

import glob
import h5py
import numpy as np


class Builder(tfds.core.GeneratorBasedBuilder):
    VERSION = tfds.core.Version('1.0.0')
    RELEASE_NOTES = {
        '1.0.0': 'Initial release.',
    }

    def _info(self) -> tfds.core.DatasetInfo:
        """Dataset metadata (homepage, citation,...)."""
        return self.dataset_info_from_configs(
            features=tfds.features.FeaturesDict({
                'steps': tfds.features.Dataset({
                    'observation': tfds.features.FeaturesDict({
                        'image': tfds.features.Image(
                            shape=(256, 256, 3),
                            dtype=np.uint8,
                            encoding_format='jpeg',
                            doc='Main camera RGB observation.',
                        ),
                        'wrist_image': tfds.features.Image(
                            shape=(256, 256, 3),
                            dtype=np.uint8,
                            encoding_format='jpeg',
                            doc='Wrist camera RGB observation.',
                        ),
                        # 'segmentation': tfds.features.Image(
                        #     shape=(256, 256, 1),
                        #     dtype=np.uint8,
                        #     doc='Main camera RGB observation.',
                        # ),
                        # 'wrist_segmentation': tfds.features.Image(
                        #     shape=(256, 256, 1),
                        #     dtype=np.uint8,
                        #     doc='Wrist camera RGB observation.',
                        # ),
                        'state': tfds.features.Tensor(
                            shape=(8,),
                            dtype=np.float32,
                            doc='Robot EEF state (6D pose, 2D gripper).',
                        ),
                        'joint_state': tfds.features.Tensor(
                            shape=(7,),
                            dtype=np.float32,
                            doc='Robot joint angles.',
                        )
                    }),
                    'action': tfds.features.Tensor(
                        shape=(7,),
                        dtype=np.float32,
                        doc='Robot EEF action.',
                    ),
                    'discount': tfds.features.Scalar(
                        dtype=np.float32,
                        doc='Discount if provided, default to 1.'
                    ),
                    'reward': tfds.features.Scalar(
                        dtype=np.float32,
                        doc='Reward if provided, 1 on final step for demos.'
                    ),
                    'is_first': tfds.features.Scalar(
                        dtype=np.bool_,
                        doc='True on first step of the episode.'
                    ),
                    'is_last': tfds.features.Scalar(
                        dtype=np.bool_,
                        doc='True on last step of the episode.'
                    ),
                    'is_terminal': tfds.features.Scalar(
                        dtype=np.bool_,
                        doc='True on last step of the episode if it is a terminal step, True for demos.'
                    ),
                    'language_instruction': tfds.features.Text(
                        doc='Language Instruction.'
                    ),
                    'object_info': tfds.features.Text(
                        doc='Object Info.'
                    )
                }),
                'episode_metadata': tfds.features.FeaturesDict({
                    'file_path': tfds.features.Text(
                        doc='Path to the original data file.'
                    ),
                }),
            }))

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        return {
            'train': self._generate_examples(glob.glob("/path/to/your/dataset/libero_90_no_noops/*.hdf5")),
        }

    def _generate_examples(self, paths):
        def _parse_example(episode_path, demo_id):
            # load raw data
            with h5py.File(episode_path, "r") as F:
                if f"demo_{demo_id}" not in F['data'].keys():
                    return None # skip episode if the demo doesn't exist (e.g. due to failed demo)
                actions = F['data'][f"demo_{demo_id}"]["actions"][()]
                states = F['data'][f"demo_{demo_id}"]["obs"]["ee_states"][()]
                gripper_states = F['data'][f"demo_{demo_id}"]["obs"]["gripper_states"][()]
                joint_states = F['data'][f"demo_{demo_id}"]["obs"]["joint_states"][()]
                images = F['data'][f"demo_{demo_id}"]["obs"]["agentview_rgb"][()]
                wrist_images = F['data'][f"demo_{demo_id}"]["obs"]["eye_in_hand_rgb"][()]
                # segmentation = F['data'][f"demo_{demo_id}"]["agentview_seg"][()]
                # wrist_segmentation = F['data'][f"demo_{demo_id}"]["eye_in_hand_seg"][()]
                object_infos = F['data'][f"demo_{demo_id}"]["object_infos"][()]

            # compute language instruction
            raw_file_string = os.path.basename(episode_path).split('/')[-1]
            words = raw_file_string[:-10].split("_")
            command = ''
            for w in words:
                if "SCENE" in w:
                    command = ''
                    continue
                command = command + w + ' '
            command = command[:-1]

            # assemble episode --> here we're assuming demos so we set reward to 1 at the end
            episode = []
            for i in range(actions.shape[0]):
                episode.append({
                    'observation': {
                        'image': np.flipud(images[i]),
                        'wrist_image': np.flipud(wrist_images[i]),
                        'state': np.asarray(np.concatenate((states[i], gripper_states[i]), axis=-1), np.float32),
                        'joint_state': np.asarray(joint_states[i], dtype=np.float32),
                    },
                    'action': np.asarray(actions[i], dtype=np.float32),
                    'discount': 1.0,
                    'reward': float(i == (actions.shape[0] - 1)),
                    'is_first': i == 0,
                    'is_last': i == (actions.shape[0] - 1),
                    'is_terminal': i == (actions.shape[0] - 1),
                    'language_instruction': command,
                    'object_info': object_infos[i],
                })

            # create output data sample
            sample = {
                'steps': episode,
                'episode_metadata': {
                    'file_path': episode_path
                }
            }

            # if you want to skip an example for whatever reason, simply return None
            return episode_path + f"_{demo_id}", sample

        # for smallish datasets, use single-thread parsing
        for sample in paths:
            with h5py.File(sample, "r") as F:
                n_demos = len(F['data'])
            idx = 0
            cnt = 0
            while cnt < n_demos:
                ret = _parse_example(sample, idx)
                if ret is not None:
                    cnt += 1
                idx += 1
                if ret is not None:
                    yield ret
