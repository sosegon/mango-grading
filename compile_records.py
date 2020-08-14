import glob
import os
import numpy as np

os.environ['MANGO_DATA_DIR'] = '/mnt/linux_shared/shared/datasets/Studio'

dataset = [['diseased', 'ripe', 'size', 'filename']]

for file in glob.glob(os.environ['MANGO_DATA_DIR'] + '/**/*.jpg', recursive=True):
    diseased = -1
    if 'disease' in file.lower():
        diseased = 1
    elif 'healthy' in file.lower():
        diseased = 0

    ripe = -1
    if 'unripe' in file.lower():
        ripe = 0
    elif 'partially ripe' in file.lower():
        ripe = 2
    elif 'ripe' in file.lower():
        ripe = 1

    size = -1
    if 'S_' in file or 'small' in file.lower():
        size = 0
    elif 'M_' in file or 'medium' in file.lower():
        size = 1
    elif 'very big' in file.lower():
        size = 3
    elif 'L_' in file or 'big' in file.lower():
        size = 2

    record = [diseased, ripe, size, file.replace(
        os.environ['MANGO_DATA_DIR'], '.')]
    dataset.append(record)

dataset = np.array(dataset)
np.savetxt('records.csv', dataset, fmt='%s', delimiter=',')
