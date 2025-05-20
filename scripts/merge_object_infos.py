import os
import shutil
from tqdm import tqdm


data_root = '/your/object_info/root'
save_root = '/your/save/root'
os.makedirs(save_root, exist_ok=True)

for data_name in os.listdir(data_root):
    if data_name == 'libero_90_no_noops':
        continue
    object_info_dir = os.path.join(data_root, data_name, 'object_infos')
    for object_info_file in tqdm(os.listdir(object_info_dir), desc=f"Processing {data_name}"):
        object_info_path = os.path.join(object_info_dir, object_info_file)
        save_path = os.path.join(save_root, object_info_file)
        if os.path.exists(save_path):
            print(f"File {save_path} already exists, skipping.")
            continue
        shutil.copy(object_info_path, save_path)
