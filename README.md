# DM-Case2
Homework1 in NCTU Digital Medicine

## Hardware
The following specs were used to create the original solution.
- Ubuntu 18.04 LTS
- Intel(R) Core(TM) i7-6700 CPU @ 3.40 GHz
- NVIDIA GeForce GTX TITAN X

## Installation
All requirements should be detailed in requirements.txt. Using Anaconda is strongly recommended. {envs_name} is the new environment name which you should assign.
```
conda create -n {envs_name} python=3.6
source activate {envs_name}
pip install -r requirements.txt
```
## Dataset Preparation
The training_label.csv is already in the data directory. You can download the data on the Kaggle website: https://www.kaggle.com/c/cs-t0828-2020-hw1/data

### Prepare Images
After downloading, the data directory is structured as:
```
data
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
```

### Data Preprocessing
It is going to split the training data randomly to generate a new training data and valid data in the data directory. The ratio of the training data and valid data is 8 : 2

```
$ python3 preprocessing.py
```

## Training
I provide 2 model for the task. One is ResNet50, and the other is DenseNet201.
You can run the ResNet50 model by following
```
$ python3 ResNet50.py
```
You can run the DenseNet201 model by following
```
$ python3 DenseNet201.py
```

## Make Submission
There are two python file to make different submission
You can run make_submission_ResNet50 to make a submission for ResNet50 model
```
$ python3 make_submission_ResNet50.py
```
You can run make_submission_ResNet50 to make a submission for DenseNet201 model
```
$ python3 make_submission_DenseNet201.py
```
