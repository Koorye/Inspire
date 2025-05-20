import os


bddl_root = '/your/libero/bddl/root'

for filename in os.listdir(bddl_root):
    if not filename.endswith('.bddl'):
        continue
    
    with open(os.path.join(bddl_root, filename), 'r') as f:
        lines = f.readlines()
    lines = [line.replace('Floor', 'Living_Room_Tabletop') for line in lines]
    lines = [line.replace('floor', 'living_room_table') for line in lines]

    with open(os.path.join(bddl_root, filename), 'w') as f:
        f.writelines(lines)
    print(f'Processed {filename}')
