import json
import os
import re
from rich import print
from tqdm import tqdm


def load_annotations_per_episode(episode_root):
    anno_dir = os.path.join(episode_root, 'anno')
    indexs = list(sorted([int(filename.split('.')[0]) for filename in os.listdir(anno_dir)]))
    annotations = []
    for index in indexs:
        anno_path = os.path.join(episode_root, 'anno', f'{index}.json')
        with open(anno_path, 'r') as f:
            annotation = json.load(f)
        annotations.append(annotation)
    return annotations


def get_objects_from_instruction(instruction):
    if re.search(r'put (.+) on (.+)', instruction):
        catch_object, place_object = re.search(r'put (.+) on (.+)', instruction).groups()
    elif re.search(r'stack (.+) on (.+)', instruction):
        catch_object, place_object = re.search(r'stack (.+) on (.+)', instruction).groups()
    elif re.search(r'put (.+) in (.+)', instruction):
        catch_object, place_object = re.search(r'put (.+) in (.+)', instruction).groups()
    elif re.search(r'move (.+) near (.+)', instruction):
        catch_object, place_object = re.search(r'move (.+) near (.+)', instruction).groups()
    elif re.search(r'push (.+) into (.+)', instruction):
        catch_object, place_object = re.search(r'push (.+) into (.+)', instruction).groups()
        place_object = None
    elif re.search(r'pull out (.+) from (.+)', instruction):
        catch_object, place_object = re.search(r'pull out (.+) from (.+)', instruction).groups()
        place_object = None
    elif re.search(r'pick (.+)', instruction):
        catch_object = re.search(r'pick (.+)', instruction).group(1)
        place_object = None
    else:
        raise ValueError(f"Instruction ({instruction}) format not recognized.")
    return {
        'catch': catch_object,
        'place': place_object,
    }


def get_coarse_direction(object_info):
    robot_pos = object_info['position']['robot']
    
    direction_dict = {}
    for obj, pos in object_info['position'].items():
        if obj == 'robot':
            continue

        if object_info['catch'][obj]:
            direction_dict[obj] = 'catch'
            continue
        
        x = pos[0] - robot_pos[0]
        y = pos[1] - robot_pos[1]
        z = pos[2] - robot_pos[2]

        if abs(x) > abs(y) and abs(x) > abs(z):
            if x > 0:
                direction_dict[obj] = 'right'
            else:
                direction_dict[obj] = 'left'
        elif abs(y) > abs(x) and abs(y) > abs(z):
            if y > 0:
                direction_dict[obj] = 'back'
            else:
                direction_dict[obj] = 'front'
        elif abs(z) > abs(x) and abs(z) > abs(y):
            if z > 0:
                direction_dict[obj] = 'up'
            else:
                direction_dict[obj] = 'down'
        else:
            direction_dict[obj] = 'down'
        
    return direction_dict


def annotate_object_infos(annotations, catch_thresh=0.75):
    objects = get_objects_from_instruction(annotations[0]['task'])
    start_catch_state = annotations[0]['state'][-1]

    # annotate robot position and catch state
    object_infos = []
    for annotation in annotations:
        pos = annotation['state'][:3]
        catch = (annotation['state'][-1] < catch_thresh * start_catch_state)
        object_infos.append({
            'catch': {},
            'position': {'robot': pos},
            'is catched': catch,
        })
        
    # estimate object position before catch
    catch_start_object_info_indexs, catch_end_object_info_indexs = [], []
    for i in range(1, len(object_infos)):
        if not object_infos[i - 1]['is catched'] and object_infos[i]['is catched']:
            catch_start_object_info_indexs.append(i)
        if object_infos[i - 1]['is catched'] and not object_infos[i]['is catched']:
            catch_end_object_info_indexs.append(i)
    
    if len(catch_end_object_info_indexs) == 0:
        print(f"Warning: No catch end points detected in task {annotations[0]['task']}, use last index.")
        catch_end_object_info_indexs.append(len(object_infos) - 1)
    
    assert len(catch_start_object_info_indexs) == 1, "Multiple catch start points detected."
    assert len(catch_end_object_info_indexs) == 1, "Multiple catch end points detected."
    catch_start_robot_position = object_infos[catch_start_object_info_indexs[0]]['position']['robot']
    catch_end_robot_position = object_infos[catch_end_object_info_indexs[0]]['position']['robot'] if len(catch_end_object_info_indexs) == 1 else None
    
    for i, object_info in enumerate(object_infos):
        if i < catch_start_object_info_indexs[0]:
            object_info['position'][objects['catch']] = catch_start_robot_position
            object_info['catch'][objects['catch']] = False
        elif i < catch_end_object_info_indexs[0]:
            object_info['position'][objects['catch']] = object_info['position']['robot']
            object_info['catch'][objects['catch']] = True
        else:
            object_info['position'][objects['catch']] = catch_end_robot_position
            object_info['catch'][objects['catch']] = False

        if objects['place'] is not None:
            object_info['position'][objects['place']] = catch_end_robot_position
            object_info['catch'][objects['place']] = False
    
    for object_info, annotation in zip(object_infos, annotations):
        annotation['object_info'] = object_info
        annotation['object_info']['coarse_direction'] = get_coarse_direction(object_info)
    
    return annotations


def save_annotations(annotations, episode_root):
    anno_dir = os.path.join(episode_root, 'anno_w_pos')
    os.makedirs(anno_dir, exist_ok=True)
    for index, annotation in enumerate(annotations):
        anno_path = os.path.join(anno_dir, f'{index}.json')
        with open(anno_path, 'w') as f:
            json.dump(annotation, f, indent=4)


def main():
    data_root = '/path/to/your/real/dataset'
        
    for episode_dir in tqdm(os.listdir(data_root), desc=f"Processing episodes"):
        episode_root = os.path.join(data_root, episode_dir)
        annotations = load_annotations_per_episode(episode_root)
        annotations = annotate_object_infos(annotations, catch_thresh=0.75)
        save_annotations(annotations, episode_root)


if __name__ == '__main__':
    main()
