# Dataset Preparation

## LIBERO

You can download processed LIBERO datasets from this [link]().

Otherwise, you can run the following commands to prepare your LIBERO datasets.

1. Download LIBERO Datasets from [LIBERO](https://libero-project.github.io/main.html)

```bash
mkdir libero-all
cd libero-all

wget https://utexas.box.com/shared/static/04k94hyizn4huhbv5sz4ev9p2h1p6s7f.zip # LIBERO-Spatial
wget https://utexas.box.com/shared/static/avkklgeq0e1dgzxz52x488whpu8mgspk.zip # LIBERO-Object
wget https://utexas.box.com/shared/static/avkklgeq0e1dgzxz52x488whpu8mgspk.zip # LIBERO-Goal
wget https://utexas.box.com/shared/static/cv73j8zschq8auh9npzt876fdc1akvmk.zip # LIBERO-100, including 90 and 10

unzip 04k94hyizn4huhbv5sz4ev9p2h1p6s7f.zip
unzip avkklgeq0e1dgzxz52x488whpu8mgspk.zip
unzip avkklgeq0e1dgzxz52x488whpu8mgspk.zip
unzip cv73j8zschq8auh9npzt876fdc1akvmk.zip

cd ..
```

After running the above commands, you will get a directory structure like:
```bash
libero-all
|
+- libero-10
|  +- xxx.hdf5
|
+- libero-90
|  +- xxx.hdf5
|
+- libero-goal
|  +- xxx.hdf5
|
+- libero-object
|  +- xxx.hdf5
|
+- libero-spatial
|  +- xxx.hdf5
```

2. Regenerate dataset, this operation will remove noops and failures, and get object relations.

```bash
task_suite_names=(
    libero_90 
    libero_goal 
    libero_spatial 
    libero_object 
    libero_10
)

for task_suite_name in "${task_suite_names[@]}"; do
	python scripts/parallel_libero_dataset_regenerator.py \
	  --num-gpus number_of_your_gpus \
	  --libero-task-suite ${libero_task_suite} \
	  --libero-raw-data-dir libero-all/${libero_task_suite} \
	  --libero-target-dir libero-all/${libero_task_suite}_no_noops 
done
```

3. Build regenerated dataset with RLDS.

Change each path in the `_split_generators` function of each RLDS dataset builder, including:
- `rlds_dataset_builder/libero_10/libero_10_dataset_builder.py`, 
- `rlds_dataset_builder/libero_90/libero_90_dataset_builder.py`, 
- `rlds_dataset_builder/libero_goal/libero_goal_dataset_builder.py`, 
- `rlds_dataset_builder/libero_object/libero_object_dataset_builder.py`,
- `rlds_dataset_builder/libero_spatial/libero_spatial_dataset_builder.py`.

```bash
cd rlds_dataset_builder/libero_90
tfds build
cd ..

cd libero_goal
tfds build
cd ..

cd libero_object
tfds build
cd ..

cd libero_spatial
tfds build
cd ..

cd libero_10
tfds build
cd ../..

mv libero-all/libero-90/object_infos ~/tensorflow_datasets/libero-90/object_infos
mv libero-all/libero-goal/object_infos ~/tensorflow_datasets/libero-goal/object_infos
mv libero-all/libero-object/object_infos ~/tensorflow_datasets/libero-object/object_infos
mv libero-all/libero-spatial/object_infos ~/tensorflow_datasets/libero-spatial/object_infos
mv libero-all/libero-10/object_infos ~/tensorflow_datasets/libero-10/object_infos
```

After running the above commands, you will get a directory structure in your home directory like:
```bash
tensorflow_datasets
|
+- libero-10
|  +- 1.0.0
|
+- libero-90
|  +- 1.0.0
|
+- libero-goal
|  +- 1.0.0
|
+- libero-object
|  +- 1.0.0
|
+- libero-spatial
|  +- 1.0.0
```

4. (Optional) If you want to train **Inspire-FAST**, you need to convert RLDS format to lerobot.

```bash
python scripts/tfds_to_lerobot.py --data-dir /your/home/tensorflow_datasets
```

## Real-world

1. Collect the data with your own robot and construct a directory structure like:
```bash
real
|
+- episode_0
|  +- img
|     +- 0.png
|     +- 1.png
|     +- ...
|  +- anno
|     +- 0.json
|     +- 1.json
|     +- ...
|
+- episode_1
|  +- ...
|
+- ...
```

Each JSON file is like:
```json
{
    "action": [
        -4058.0,
        -52250.0,
        336503.0,
        -172566.0,
        42634.0,
        96400.0,
        69300.0
    ],
    "state": [
        -2843.0,
        -52329.0,
        336502.0,
        -172493.0,
        42622.0,
        97746.0,
        69300.0
    ],
    "task": "move the can near the apple"
}
```

Where state and action is a 7-dim list contains [x, y, z, rx, ry, rz, gripper], each element in state is a absolute world position.

2. Annotate dataset.

```bash
python scripts/annotate_data.py
```

After running the above command, you dataset structure will be like:
```bash
|
+- episode_0
|  +- img
|     +- 0.png
|     +- 1.png
|     +- ...
|  +- anno
|     +- 0.json
|     +- 1.json
|     +- ...
|  +- anno_w_pos
|     +- 0.json
|     +- 1.json
|     +- ...
|
+- episode_1
|  +- ...
|
+- ...
```

And JSON file will be like:
```json
{
    "action": [
        -4058.0,
        -52250.0,
        336503.0,
        -172566.0,
        42634.0,
        96400.0,
        69300.0
    ],
    "state": [
        -2843.0,
        -52329.0,
        336502.0,
        -172493.0,
        42622.0,
        97746.0,
        69300.0
    ],
    "task": "move the can near the apple",
    "object_info": {
        "catch": {
            "the can": false,
            "the apple": false
        },
        "position": {
            "robot": [
                -2843.0,
                -52329.0,
                336502.0
            ],
            "the can": [
                -156676.0,
                -175687.0,
                141998.0
            ],
            "the apple": [
                -66238.0,
                -258794.0,
                133875.0
            ]
        },
        "is catched": false,
        "coarse_direction": {
            "the can": "down",
            "the apple": "front"
        }
    }
}
```

3. Finally, write your own dataset builder to construct your own dataset into RLDS or libero format. 