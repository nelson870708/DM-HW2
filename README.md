# DM-Case2
Project in Digital Medicine in NCTU

## Hardware
The following specs were used to create the original solution.
- Ubuntu 18.04 LTS
- Intel(R) Core(TM) i7-6700 CPU @ 3.40 GHz
- NVIDIA GeForce GTX TITAN X

## Installation
All requirements should be detailed in requirements.txt. Using Anaconda is strongly recommended. {envs_name} is the new environment name which you should assign.
```
conda create -n {envs_name} python=3.7
source activate {envs_name}
pip install -r requirements.txt
```
## Dataset Preparation
You can download the data on the following google drive: 

Training data: https://drive.google.com/file/d/1xd7gpJjJ9rJy8XqW1ArfAtkzXr1rvroL/view?usp=sharing

Testing data: https://drive.google.com/file/d/1xd7gpJjJ9rJy8XqW1ArfAtkzXr1rvroL/view?usp=sharing
### Prepare Images
After downloading, the data directory is structured as:
```
TrainingData
  +- epidural
    +- ID_0a5b19112.jpg
    +- ID_0a21c7cde.jpg
    ...
  +- healthy
    +- ID_0a0f3abd0.jpg
    +- ID_0acc9d2bf.jpg
    ...
  +- intraparenchymal
    +- ID_00a1d04a4.jpg
    +- ID_0a1dc9169.jpg
    ...
  +- intraventricular
    +- ID_0a5db43bf.jpg
    +- ID_0a729be82.jpg
    ...
  +- subarachnoid
    +- ID_0a0b55bbd.jpg
    +- ID_0a7ba802a.jpg
    ...
  +- subdural
    +- ID_0a4a21efb.jpg
    +- ID_0a16f9f35.jpg
    ...
+- TestingData
  +- Test_001.dcm
  +- Test_002.dcm
  ...
```

### Data Preprocessing
First, it will transfer the dicom file to jpg file. And, it is going to do the data augmentation. Finally, it is going to split the data randomly to generate a training data and valid data in the input directory. The ratio of the training data and valid data is 8 : 2

```
$ python3 preprocessing.py
```

## Training
You can do training by following
```
$ python3 training.py
```

## Make Submission / Testing
You can do testing by following 
```
$ python3 testing.py
```
