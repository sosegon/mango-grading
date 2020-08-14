# Mango analysis

The content of this repo is based on the work by [Pandey R. et al](https://ieeexplore.ieee.org/abstract/document/6968366).

The project consists of analysing images of mangos to determine their health, maturity and quality. The majority of the work is about processing and assessing the color of images in different spaces.

Detailed explanation of the code is in this [post](https://bit.ly/avaiMangosOpenCV) (Spanish).

## Dataset

The original dataset is in this [page](https://data.mendeley.com/datasets/fmfncxjz3v/1). However, the images are not compiled. Also, when the data is extracted, the folder structure is not the same shown in the download page. Therefore, the compiled dataset is [here](https://drive.google.com/file/d/10kVRZI0Op3MilofTMWnmlf7E109EJNYu/view?usp=sharing).

## How to use the code

To run the code locally it is necessary to clone this repo:

`git clone git@github.com:sosegon/mango-grading`

The main code is under the file [mango_analyser.py](./mango_analyser.py). However, the complete analysis is located in the notebook [Analysis.ipynb](./Analysis.ipynb).

It is necessary to create a virtual environment using [Anaconda](https://www.anaconda.com/products/individual). The dependencies are in the file [env.yml](./env.yml):

`conda env create -f env.yml`

Then, the environment has to be activated:

`source activate mango-grading`

Finally, jupyter has to start:

`jupyter notebook`


## Warnings

- In the cell code under the section *Analyse every mango image* in the notebook, the following line:

    `init_path = '/mnt/linux_shared/shared/datasets/Studio'`

    has to be updated with the location where the dataset was uncompressed.

- The code of this project does not guarantee the same results in the original work. Also, the results in other images may be inadequate.




