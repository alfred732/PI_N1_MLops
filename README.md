# Bienvenido al repositorio de mi proyecto 😎!
<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

Este es mi primer proyecto de **"Sistema de Recomendación de películas con Machine Learning + FastAPI"**, también es el primer proyecto de los "PI"(Proyecto Individual) de Labs.
Todo el proyecto esta propuesto en:
https://github.com/HX-PRomero/PI_ML_OPS/blob/main/Readme.md
## Objetivo

La finalidad de este proyecto es proporcionar una interfaz API para acceder y consultar información sobre películas, ademas, cuenta con un sistema de recomendación usando machine learning

## Archivos

|Archivo| Descripción
|--|--|
|**transformaciones.ipynb**|Muestra todo el proceso de ETL del proyecto en base a los datos en "credits.csv" y "movies_dataset.csv, siguiendo los pasos propuestos|  |
|**funcionesApi.ipynb**|Se muestra las funciones 6 funciones empleadas en la API|
|**EDA.ipynb**|Muestra como generar un informe de análisis exploratorio de los datos transformados
|**sistema_recom.ipynb**|Muestra los pasos para crear el sistema de recomendación de películas. |
|**main.py** |Código final que se usara para montar la API en FastApi, incluye las 6 funciones + 1 función del sistema de recomendación.|

Todos los archivos se encuentran comentados para una facil comprension.


## Guia FastAPi

Para ejecutar el codigo y montar la API, necesitaremos las siguientes bibliotecas:
**FastAPI:**
`$ pip install fastapi`   

**Uvicorn:**
`$ pip install "uvicorn[standard]"`   

Una vez instalado, abriremos una nueva terminal y ejecutaremos el siguiente **codigo** para activar la API:

`$ uvicorn main:app --reload --port 8000`   
> **Note:** Asegurarnos de estar en el directorio donde se encuentra el archivo  ( main.py ).


    INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)  
    INFO: Started reloader process [28720]  
    INFO: Started server process [28722]  
    INFO: Waiting for application startup.  
    INFO: Application startup complete.
Una vez completado debemos dirigirnos a la direccion que nos muestra, pero mejor nos dirigimos a la API interactiva:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

<img  src="https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png"  alt="Texto alternativo">

**Para obtener una mejor guia de uso y la documentacion:**
https://fastapi.tiangolo.com/

## Referencias

Video en el cual se baso el sistema de recomendacion:

https://www.youtube.com/watch?v=7rEagFH9tQg&t=624s
"Project 18. Movie Recommendation System using Machine Learning with Python"

