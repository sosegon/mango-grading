# Análisis de mangos

El contenido de este repositorio está basado en el trabajo de [Pandey R. et al](https://ieeexplore.ieee.org/abstract/document/6968366).

El proyecto consiste en el análisis de imágenes de mangos para determinar su estado de salud, madurez y calidad. La mayor parte del trabajo se basa en el análisis de color de las imágenes en diferentes espacios de color.

Explicación detallada del código se encuentra en [este artículo](https://bit.ly/avaiMangosOpenCV).

## Dataset

El dataset original está en está [paǵina](https://data.mendeley.com/datasets/fmfncxjz3v/1). Sin embargo, las imágenes no están compiladas y al extraer los datos, la estructura no es la misma que se muestra en la página de descarga. Así que el dataset compilado está [aquí](https://drive.google.com/file/d/10kVRZI0Op3MilofTMWnmlf7E109EJNYu/view?usp=sharing).

## Cómo usar el código

Para ejecutar el código localmente, es necesario clonar el repositorio

`git clone git@github.com:sosegon/mango-grading`


El código principal está en el archivo [mango_analyser.py](./mango_analyser.py). Sin embargo, el análisis completo está en el notebook [Analysis.ipynb](./Analysis.ipynb).

Para ejecutar el código es necesario crear un ambiente virtual usando [Anaconda](https://www.anaconda.com/products/individual). Las depencias se encuentran en el archivo [env.yml](./env.yml)

`conda env create -f env.yml`

Luego, se activa el ambiente virtual

`source activate mango-grading`

Se inicia jupyter

`jupyter notebook`


## Advertencias

- En la celda de código de la sección *Analyse every mango image* del notebook, la línea

    `init_path = '/mnt/linux_shared/shared/datasets/Studio'`

    tiene que ser actualizada con la dirección donde fue descomprimido el dataset.

- El código de este proyecto no garantiza los mismos resultados del trabajo original. Igualmente, los resultados en otras imágenes podrían ser poco adecuados.




