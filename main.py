from fastapi import FastAPI
from typing import Optional
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

app = FastAPI()
df = pd.read_csv('PeliculasCreditos2.csv', parse_dates=['release_date'])

#-----------------------------------------------------------------------------

@app.get("/cantidad_filmaciones_mes")
def get_cantidad_filmaciones_mes(mes: str):
    cantidad = cantidad_filmaciones_mes(mes)
    return {"cantidad": cantidad}

def cantidad_filmaciones_mes(mes: str):
    # Mapeo de nombres de meses en español a inglés
    meses_espanol = {
        'enero': 'January',
        'febrero': 'February',
        'marzo': 'March',
        'abril': 'April',
        'mayo': 'May',
        'junio': 'June',
        'julio': 'July',
        'agosto': 'August',
        'septiembre': 'September',
        'octubre': 'October',
        'noviembre': 'November',
        'diciembre': 'December'
    }
    # Convertir el mes a número en inglés
    mes_numero = pd.to_datetime(meses_espanol[mes.lower()], format='%B').month
    cantidad = sum(df['release_date'].dt.month == mes_numero)    
    return cantidad

@app.get("/cantidad_filmaciones_dia")
def get_cantidad_filmaciones_dia(dia: str):
    cantidad = cantidad_filmaciones_dia(dia)
    return {"cantidad": cantidad}

def cantidad_filmaciones_dia(dia: str):
    # Mapeo de nombres de días en español a inglés
    dias_espanol = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }

    # Convertir el día a nombre en inglés
    dia_ingles = dias_espanol[dia.lower()]

    # Filtrar el DataFrame por el día de estreno
    cantidad = sum(df['release_date'].dt.strftime('%A') == dia_ingles)

    # Devolver las películas del día
    return cantidad

@app.get("/score_titulo")
def get_score_titulo(titulo: str):
    resultado = score_titulo(titulo)
    return resultado

def score_titulo(titulo: str):
    pelicula = df[df['title'] == titulo]
    
    anio_estreno = pelicula['release_year'].values[0]
    score = pelicula['popularity'].values[0]

    respuesta = {
        "titulo": titulo,
        "anio_estreno": int(anio_estreno),
        "score": float(score)
    }
    return respuesta

@app.get("/get_actor")
def get_actor_endpoint(nombre_actor: str):
    resultado = get_actor(df, nombre_actor)
    if resultado is None:
        return {"mensaje": "El actor no se encuentra en la lista de actores."}
    else:
        nombre_actor, cantidad_pelis, retorno_total, promedio_retorno = resultado
        return {
            "nombre_actor": nombre_actor,
            "cantidad_pelis": cantidad_pelis,
            "retorno_total": retorno_total,
            "promedio_retorno": promedio_retorno
        }

@app.get("/votos_titulo")
def votos_titulo_endpoint(titulo: str):
    resultado = votos_titulo(df, titulo)
    if resultado is None:
        return {"mensaje": "No se encontró ninguna película con ese título o no cumple con la condición mínima de 2000 valoraciones."}
    else:
        titulo, votos, promedio_votos = resultado
        return {
            "titulo": titulo,
            "votos": votos,
            "promedio_votos": promedio_votos
        }

def votos_titulo(df, titulo):
    pelicula = df[df['title'] == titulo]

    if len(pelicula) == 0:
        return None

    votos = pelicula['vote_count'].values[0]
    promedio_votos = pelicula['vote_average'].values[0]

    if votos < 2000:
        return None

    return titulo, votos, promedio_votos

def get_actor(df, nombre_actor):
    actor = df[df['cast'].apply(lambda x: isinstance(x, str) and nombre_actor in x)]
    
    if len(actor) == 0:
        return None
    
    cantidad_pelis = len(actor)
    retorno_total = actor['return'].sum()
    promedio_retorno = retorno_total / cantidad_pelis

    return nombre_actor, cantidad_pelis, retorno_total, promedio_retorno

@app.get("/get_director")
def get_director_endpoint(nombre_director: str):
    resultado = get_director(df, nombre_director)
    if resultado is None:
        return {"mensaje": "El director no se encuentra en el dataset."}
    else:
        exito_director, peliculas_director = resultado
        return {
            "exito_director": exito_director,
            "peliculas_director": peliculas_director.to_dict(orient='records')
        }

def get_director(df, nombre_director):
    director = df[df['Director'] == nombre_director]

    if len(director) == 0:
        return None

    exito_director = director['return'].sum()
    
    peliculas_director = director[['title', 'release_date', 'return', 'budget','revenue']]

    return exito_director, peliculas_director

@app.get("/recomendar_pelicula/{movie_name}")
def recomendar_pelicula(movie_name: str):
    lista_de_todas_las_peliculas = peliculas['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, lista_de_todas_las_peliculas)
    close_match = find_close_match[0]
    index_of_the_movie = peliculas[peliculas['title'] == close_match]['ID'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    recommended_movies = []
    i = 1
    for movie_name in sorted_similar_movies:
        index = movie_name[0]
        matching_rows = peliculas[peliculas.ID == index]
        if len(matching_rows) > 0:
            title_from_index = matching_rows['title'].values[0]
            recommended_movies.append(title_from_index)
            if i >= 5:
                break
            i += 1
    return {"recommended_movies": recommended_movies}

peliculas = pd.read_csv('PeliculasCreditos2.csv')
peliculas['ID'] = range(1, len(peliculas) + 1)

peliculas = peliculas.replace(',', '', regex=True)

selected_features = ['genres', 'tagline', 'cast', 'Director']

for feature in selected_features:
    peliculas[feature] = peliculas[feature].fillna('')

peliculas_combinadas = peliculas[selected_features].apply(lambda row: ' '.join(row.astype(str)), axis=1)

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(peliculas_combinadas)

similarity = cosine_similarity(feature_vectors[:2500, :])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)