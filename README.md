# CMPE 789: VOS with Cutie

This repository serves as a submission for the RIT CMPE 789: Robot Perception Final Examination. In this repository, Cutie was retrained using MOTS and used to segment a video of track runners.

Original Paper by Ho Kei Chen, et. al: Putting the Object Back into Video Object Segmentation

[[arXiV]](https://arxiv.org/abs/2310.12982) [[PDF]](https://arxiv.org/pdf/2310.12982.pdf) [[Project Page]](https://hkchengrex.github.io/Cutie/) 

## Installation

Tested on Ubuntu only.

**Prerequisite:**

- Python 3.8+
- PyTorch 1.12+ and corresponding torchvision

**Clone this repository:**

```bash
git clone https://github.com/asp6244/CMPE789_VOSwCutie.git
cd Cutie
```

**Create the conda environment:**

```bash
conda create --name Cutie --file requirements.yml
conda activate Cutie
```

**Install with pip:**

```bash
pip install -e .
```

**Download the pretrained models:**

```bash
python scripts/download_models.py
```

### Download MOTS and test_data:

- (MOTS not required for evaluation)
- MOTS: https://motchallenge.net/data/MOTS/
- test data: https://drive.google.com/file/d/1xb_HRr80JDGfxG69eRLZBg6FX-INB0y8/view?usp=drive_link
- Place the data one level higher than the Cutie root directory with the following datastructure:

```bash
├── CMPE789_VOSwCutie
├── MOTS
│   ├── test
│   └── train
│       ├── JPEGImages
│       │   ├── MOTS20-02
│       │   │   ├── 000001.jpg
│       │   │   └── ...
│       │   ├── MOTS20-05
│       │   │   ├── 000001.jpg
│       │   │   └── ...
│       │   ├── MOTS20-09
│       │   │   ├── 000001.jpg
│       │   │   └── ...
│       │   └── MOTS20-11
│       │       ├── 000001.jpg
│       │       └── ...
│       │   
│       ├── Annotations
│       │   ├── MOTS20-02
│       │   ├── MOTS20-05
│       │   ├── MOTS20-09
│       │   └── MOTS20-11
│       │
│       ├── MOTS20-02_gt.txt
│       ├── MOTS20-05_gt.txt
│       ├── MOTS20-09_gt.txt
│       └── MOTS20-11_gt.txt
│
└── test_data
    ├── JPEGImages
    │   └── runner
    │       ├── 00000000.jpg
    │       └── ...
    └── Annotations
        └── runner
            └── 00000000.png
```

**Download and install the coco mask API; necessary to use MOTS:**
- Location of the directory does not matter
```bash
git clone https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI
python setup.py build_ext --inplace
```

**Create the MOTS ground-truth masks:**
```bash
python openMOTS.py
```

# Training

## Train the model using MOTS

**Modify the training config in:**
- cutie/config/train_config.yaml
- cutie/config/data/custom.yaml
- cutie/config/data/datasets.yaml

### Begin training

```bash
OMP_NUM_THREADS=4 torchrun --master_port 25357 --nproc_per_node=1 cutie/train.py
```
- Trained model will be in `output/default/`

**If training using more than one GPU or node:**
- Modify the `local rank` and `world size` in `cutie/train.py` and `cutie/dataset/setup_training_data.py`
- Set `nproc_per_node` to the number of GPUs

## Evaluate the model using the test data

**Modify the evaluation config in:**
- cutie/config/eval_config.yaml

### Run the evaluation
```bash
python cutie/eval_vos.py dataset=generic image_directory=../test_data/JPEGImages mask_directory=../test_data/Annotations size=480
```
- Annotations will be in `output/default/generic/Annotations/runner`

Run create_video.py to create an mp4 from the annotated images
```bash
python create_video.py
```
- Video output will be in `output/default/generic/Annotations`


## Additional Instructions

1. [Running Cutie on video object segmentation data.](docs/EVALUATION.md)
2. [Training Cutie.](docs/TRAINING.md)
