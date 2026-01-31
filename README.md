# Inspire

Official implementation of the paper "[InSpire: Vision-Language-Action Models with Intrinsic Spatial Reasoning](https://arxiv.org/abs/2505.13888)".

> **Note**: We are doing our best to improve this work. If you have any questions or suggestions, please feel free to create an issue in this repo or contact us at shihan.wu.koorye@outlook.com.

[[Project]](https://Koorye.github.io/proj/Inspire/) [[ArXiv]](https://arxiv.org/abs/2505.13888) [[PDF]](https://arxiv.org/pdf/2505.13888) [[Inspire-FAST]](https://github.com/Koorye/Inspire-FAST)

## News

- 🔥**Feb 1, 2026**: 🎉🎉Our paper has been accepted by **ICRA 2026**!🎉🎉
- 🔥**Sep 29, 2025**: CALVIN evaluation experiment results are now available.
- 🔥**May 23, 2025**: Our paper has been updated for better clarity and readability. The optimized version is now available on [arXiv](https://arxiv.org/abs/2505.13888).
- 🔥**May 21, 2025**: The code is released and the paper is now available on [arXiv](https://arxiv.org/abs/2505.13888v1).

## Introduction

> **Abstract** Leveraging pretrained Vision-Language Models (VLMs) to map language instruction and visual observations to raw low-level actions, Vision-Language-Action models (VLAs) hold great promise for achieving general-purpose robotic systems. Despite their advancements, existing VLAs tend to spuriously correlate task-irrelevant visual features with actions, limiting their generalization capacity beyond the training data. To address this challenge, we propose Intrinsic Spatial Reasoning (InSpire), which mitigates the adverse effects of spurious correlations by boosting the spatial reasoning ability of VLAs. Specifically, InSpire redirects the model's attention to task-relevant visual clues by simply appending the question *“In which direction is the [object] relative to the robot”* before the language instruction and aligning the VLA's answer *“right / left / up / down / front / back / grasp”* and predicted actions with the ground-truth. Notably, InSpire can be employed as a plugin to enhance existing autoregressive VLAs, requiring no extra data or interaction with other large models. Extensive experimental results in both simulation and real-world environments demonstrate the effectiveness and flexibility of our approach.

![Motivation](examples/motivation.png)
![Method](examples/method.png)

## Experiments

### Overall Performance

**Real-world Environments**

![Real-world Environments](examples/real_results.png)

**LIBERO Simulated Environments**

![Simulated Environments](examples/libero_results.png)

**CALVIN Simulated Environments**

<img src="examples/calvin1.png" alt="CALVIN Results" width="50%"/><img src="examples/calvin2.png" alt="CALVIN Results" width="50%"/>

<img>

## Attention Maps

![Attention Maps](examples/attention.png)

## Videos

### Real-world Environments

> **Note**: The real-world experiment was conducted on the $\pi_0$-FAST model, and the relevant code is available at [Inspire-FAST](https://github.com/Koorye/Inspire-FAST).

**Seen Tasks**

| $\pi_0$-FAST:<br>Cookies Towel | $\pi_0$-FAST:<br>Left Bowl on Middle Bowl | $\pi_0$-FAST:<br>Blue Cup Plate | $\pi_0$-FAST:<br>Pull Bottom Plate |
|:------------------------:|:---------------------------------:|:------------------------:|:--------------------------:|
| ![Seen Cookies Towel](examples/videos/main/real/baseline/cookies_towel.gif) | ![Seen Left Bowl on Middle Bowl](examples/videos/main/real/baseline/left_bowl_on_middle_bowl.gif) | ![Seen Blue Cup Plate](examples/videos/main/real/baseline/blue_cup_plate.gif) | ![Seen Pull Bottom Plate](examples/videos/main/real/baseline/pull_bottom_plate.gif) |
| **InSpire:<br>Cookies Towel** | **InSpire:<br>Left Bowl on Middle Bowl** | **InSpire:<br>Blue Cup Plate** | **InSpire:<br>Pull Bottom Plate** |
| ![Seen Cookies Towel](examples/videos/main/real/inspire/cookies_towel.gif) | ![Seen Left Bowl on Middle Bowl](examples/videos/main/real/inspire/left_bowl_on_middle_bowl.gif) | ![Seen Blue Cup Plate](examples/videos/main/real/inspire/blue_cup_plate.gif) | ![Seen Pull Bottom Plate](examples/videos/main/real/inspire/pull_bottom_plate.gif) |

**Unseen Tasks**

| $\pi_0$-FAST:<br> Pick Orange | $\pi_0$-FAST:<br>Banana Towel | $\pi_0$-FAST:<br>Ball Book | $\pi_0$-FAST:<br>Orange Cup Plate |
|:------------------------:|:------------------------:|:-----------------------:|:--------------------------:|
| ![Unseen Pick Orange](examples/videos/main/real/baseline/pick_orange.gif) | ![Unseen Banana Towel](examples/videos/main/real/baseline/banana_towel.gif) | ![Unseen Ball Book](examples/videos/main/real/baseline/ball_book.gif) | ![Unseen Orange Cup Plate](examples/videos/main/real/baseline/orange_cup_plate.gif) |
| **InSpire:<br>Pick Orange** | **InSpire:<br>Banana Towel** | **InSpire:<br>Ball Book** | **InSpire:<br>Orange Cup Plate** |
| ![Unseen Pick Orange](examples/videos/main/real/inspire/pick_orange.gif) | ![Unseen Banana Towel](examples/videos/main/real/inspire/banana_towel.gif) | ![Unseen Ball Book](examples/videos/main/real/inspire/ball_book.gif) | ![Unseen Orange Cup Plate](examples/videos/main/real/inspire/orange_cup_plate.gif) |

### Simulated Environments

**Seen Tasks**

| miniVLA:<br>Butter Drawer | miniVLA:<br>Moka Stove | miniVLA:<br>Sauce Tray | miniVLA:<br>Book Caddy |
|:----------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
| ![Libero-90 Butter Drawer](examples/videos/main/libero/baseline/90_butter_drawer.gif) | ![Libero-90 Moka Stove](examples/videos/main/libero/baseline/90_moka_stove.gif) | ![Libero-90 Sauce Tray](examples/videos/main/libero/baseline/90_sauce_tray.gif) | ![Libero-90 Book Caddy](examples/videos/main/libero/baseline/90_book_caddy.gif) |
| **InSpire:<br>Butter Drawer** | **InSpire:<br>Moka Stove** | **InSpire:<br>Sauce Tray** | **InSpire:<br>Book Caddy** |
| ![Libero-90 Butter Drawer](examples/videos/main/libero/inspire/90_butter_drawer.gif) | ![Libero-90 Moka Stove](examples/videos/main/libero/inspire/90_moka_stove.gif) | ![Libero-90 Sauce Tray](examples/videos/main/libero/inspire/90_sauce_tray.gif) | ![Libero-90 Book Caddy](examples/videos/main/libero/inspire/90_book_caddy.gif) |


**Unseen Tasks**

| miniVLA:<br>Bowl Plate | miniVLA:<br>Cheese Basket | miniVLA:<br>Bowl Plate | miniVLA:<br>Book Caddy |
|:----------------------------:|:------------------------------:|:---------------------------:|:-------------------------:|
| ![Libero-Goal Bowl Plate](examples/videos/main/libero/baseline/goal_bowl_plate.gif) | ![Libero-Object Cheese Basket](examples/videos/main/libero/baseline/object_cheese_basket.gif) | ![Libero-Spatial Bowl Plate](examples/videos/main/libero/baseline/spatial_bowl_plate.gif) | ![Libero-10 Book Caddy](examples/videos/main/libero/baseline/10_book_caddy.gif) |
| **InSpire:<br>Bowl Plate** | **InSpire:<br>Cheese Basket** | **InSpire:<br>Bowl Plate** | **InSpire:<br>Book Caddy** |
| ![Libero-Goal Bowl Plate](examples/videos/main/libero/inspire/goal_bowl_plate.gif) | ![Libero-Object Cheese Basket](examples/videos/main/libero/inspire/object_cheese_basket.gif) | ![Libero-Spatial Bowl Plate](examples/videos/main/libero/inspire/spatial_bowl_plate.gif) | ![Libero-10 Book Caddy](examples/videos/main/libero/inspire/10_book_caddy.gif) |

## CALVIN Simulated Environments

**ABC -> D**

| miniVLA | InSpire | 
| :-------------------------:|:-------------------------:|
| ![](examples/videos/main/calvin/seq7_success0.gif) | ![](examples/videos/main/calvin/seq7_success5.gif) |
| ![](examples/videos/main/calvin/seq179_success0.gif) | ![](examples/videos/main/calvin/seq179_success5.gif) |

## Models Checkpoints

| Model | Dataset | Checkpoint |
|-------|---------|------------|
| MiniVLA | Libero90 | [Download](https://huggingface.co/InspireVLA/minivla-libero-90) |
| InspireVLA | Libero90 | [Download](https://huggingface.co/InspireVLA/minivla-inspire-libero-90) |
| InspireVLA | Libero10+Goal+Object+Spatial | [Download](https://huggingface.co/InspireVLA/minivla-inspire-libero-union4) |

## Installation

1. Clone the repository.

```bash
git clone https://github.com/Koorye/Inspire.git
```

2. Install the dependencies.

```bash
conda create -n inspire python=3.10
conda activate inspire

cd LIBERO
pip install -r requirements.txt
pip install -e .
cd ..

cd vq_bet_official
pip install -r requirements.txt
pip install -e .
cd ..

pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements-min.txt

# (Optional) for Flash Attention
pip install packaging ninja
ninja --version; echo $?  # Verify Ninja --> should return exit code "0"
pip install "flash-attn==2.5.5" --no-build-isolation
```

## Evaluation with Pretrained Checkpoints

1. Create `.hf_token` file in the root directory and add your Hugging Face token.

```bash
echo "your_huggingface_token" > .hf_token
```

2. Download pretrained checkpoints.

```bash
bash scripts/download_pretrained_weights.sh
```

3. Run the evaluation script.

```bash
bash vla_scripts/eval/eval_baseline_libero90.sh
bash vla_scripts/eval/eval_inspire_libero90.sh
```

## Training Your Own Checkpoints

1. Prepare the dataset.

See [Dataset Preparation](DATASET.md).

2. Run the training script.

```bash
bash vla_scripts/train/train_baseline_libero90.sh
bash vla_scripts/train/train_inspire_libero90.sh
```

3. Run the evaluation script.

```bash
bash vla_scripts/eval/eval_baseline_libero90.sh
bash vla_scripts/eval/eval_inspire_libero90.sh
```

## Acknowledgements

Our work is built upon the following open-source projects: [CALVIN](https://github.com/mees/calvin), [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO), [miniVLA](https://github.com/Stanford-ILIAD/openvla-mini), [Pi-0](https://github.com/Physical-Intelligence/openpi). We thank the authors for releasing their code. If you use our model and code, please consider citing these works as well.
