import os
import pydicom as dicom
from sklearn.utils import shuffle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

def preprocessing(input_dir, output_dir, target):
    for dir_path, dir_name, file_name in os.walk(input_dir):
        for f in file_name:
            file_path = os.path.join(dir_path, f)
            if len(file_path) > 25:
                file_path_list.append(file_path)
    file_path_list = shuffle(file_path_list)

    wrongsize = 0
    nullpic = 0
    excepts = 0

    null_rate = 0.9
    cap = 90
    floor = 45
    bias = 75

    data_num = len(file_path_list)
    
    for idx in range(data_num):
        wip_time = time.time()
        wip = wip_time - start
        if (idx + 1) % 10 == 0:
            remain = int((wip / (idx + 1)) * (data_num - idx))
            print('in progress %d/%d, remaining time: %d hr %d min %d sec'
                  % (idx + 1, data_num, remain // 3600, (remain % 3600) // 60, remain % 60))
        try:
            ds = dicom.dcmread(file_path_list[idx])
            slope = ds.RescaleSlope
            intercept = ds.RescaleIntercept
        except:
            excepts += 1
            continue
        pixel_array_numpy = ds.pixel_array
        length = len(pixel_array_numpy)
        if length != 512:
            print('wrong size: skipped')
            wrongsize += 1
            continue

        iszero = 0
        lst_in_hu_r = []
        lst_in_hu_g = []
        lst_in_hu_b = []
        for lst in pixel_array_numpy:
            adj_lst_r = []
            adj_lst_g = []
            adj_lst_b = []
            for i in lst:
                hu = i * slope + intercept
                if hu > 128:
                    adj_lst_r.append(255)
                    adj_lst_g.append(255)
                    adj_lst_b.append(255)
                elif hu < 0:
                    adj_lst_r.append(0)
                    adj_lst_g.append(0)
                    adj_lst_b.append(0)
                    iszero += 1
                elif hu < cap and hu > floor:
                    adj_lst_r.append(min(int(pow(hu, 2) / 64) + bias, 255))
                    adj_lst_g.append(max(hu * 2 - bias, 0))
                    adj_lst_b.append(max(int(pow(hu * 2, 1 / 2) * 16) - bias, 0))
                else:
                    adj_lst_r.append(min(int(pow(hu, 2) / 64), 255))
                    adj_lst_g.append(min(hu * 2, 255))
                    adj_lst_b.append(min(int(pow(hu * 2, 1 / 2) * 16), 255))
            lst_in_hu_r.append(adj_lst_r)
            lst_in_hu_g.append(adj_lst_g)
            lst_in_hu_b.append(adj_lst_b)
        if target == 'training':
            if iszero > 512 ** 2 * null_rate:
                nullpic += 1
                print('null: %d' % nullpic)
                continue
        np_hu_r = np.array(lst_in_hu_r).reshape((512, 512, 1))
        np_hu_g = np.array(lst_in_hu_g).reshape((512, 512, 1))
        np_hu_b = np.array(lst_in_hu_b).reshape((512, 512, 1))
        np_hu = np.concatenate((np_hu_b, np_hu_g, np_hu_r), axis=2)

        dcm_file_path = file_path_list[idx].split('/')
        if target == 'training':
            if idx < data_num * 0.8:
                file_path = os.path.join(jpg_dir, 'train', dcm_file_path[2], dcm_file_path[3].replace('.dcm', '.jpg'))
            else:
                file_path = os.path.join(jpg_dir, 'val', dcm_file_path[2], dcm_file_path[3].replace('.dcm', '.jpg'))
        else:
            file_path = os.path.join(jpg_dir, dcm_file_path[2].replace('.dcm', '.jpg'))
        cv2.imwrite(file_path, np_hu)

    end = time.time()
    total_time = end - start
    print(' ')
    print('==========finished==========')
    print('Task report:')
    print('Total time: %d hr %d min %d sec' % (total_time // 3600, (total_time % 3600) // 60, total_time % 60))
    print('Wrong size: %d' % wrongsize)
    print('Null images: %d' % nullpic)
    print('except: %d' % excepts)
    print('Total images: %d' % (data_num - wrongsize - nullpic - excepts))

start = time.time()
file_path_list = []

data_dir = './TrainingData'
jpg_dir = './input'
if not os.path.isdir('./input'):
    os.mkdir('./input')
if not os.path.isdir('./input/train'):
    os.mkdir('./input/train')
if not os.path.isdir('./input/train/epidural'):
    os.mkdir('./input/train/epidural')
if not os.path.isdir('./input/train/healthy'):
    os.mkdir('./input/train/healthy')
if not os.path.isdir('./input/train/intraparenchymal'):
    os.mkdir('./input/train/intraparenchymal')
if not os.path.isdir('./input/train/intraventricular'):
    os.mkdir('./input/train/intraventricular')
if not os.path.isdir('./input/train/subarachnoid'):
    os.mkdir('./input/train/subarachnoid')
if not os.path.isdir('./input/train/subdural'):
    os.mkdir('./input/train/subdural')
if not os.path.isdir('./input/val'):
    os.mkdir('./input/val')
if not os.path.isdir('./input/val/epidural'):
    os.mkdir('./input/val/epidural')
if not os.path.isdir('./input/val/healthy'):
    os.mkdir('./input/val/healthy')
if not os.path.isdir('./input/val/intraparenchymal'):
    os.mkdir('./input/val/intraparenchymal')
if not os.path.isdir('./input/val/intraventricular'):
    os.mkdir('./input/val/intraventricular')
if not os.path.isdir('./input/val/subarachnoid'):
    os.mkdir('./input/val/subarachnoid')
if not os.path.isdir('./input/val/subdural'):
    os.mkdir('./input/val/subdural')
 
preprocessing(data_dir, jpg_dir, 'training')

start = time.time()
file_path_list = []

data_dir = './TestingData'
jpg_dir = './test_input'
if not os.path.isdir('./test_input'):
    os.mkdir('./test_input')

preprocessing(data_dir, jpg_dir, 'testing')


