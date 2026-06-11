import pandas as pd
import os

# aqui definimos las rutas de los archivos que vamos a usar
DATA_DIR   = os.path.dirname(os.path.abspath(__file__))
CR_FILE    = os.path.join(DATA_DIR, "Outscraper-20260607153436s0a.csv")
IMDB_FILE  = os.path.join(DATA_DIR, "IMDB Dataset SPANISH.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "corpus_unificado_resenas.csv")


def obtener_polaridad(rating):
    # de 4 a 5 estrellas lo ponemos como positivo
    if rating >= 4:
        return "positivo"
    # de 1 a 2 estrellas lo ponemos como negativo
    elif rating <= 2:
        return "negativo"
    # 3 estrellas lo dejamos neutral
    else:
        return "neutral"


def cargar_google_maps(path=CR_FILE):
    # cargamos el csv de google maps
    cr = pd.read_csv(path)

    # seleccionamos unicamente las columnas que nos interesan
    cr = cr[["review_text", "review_rating", "review_datetime_utc"]].copy()

    # renombramos las columnas para que tengan un nombre mas limpio
    cr = cr.rename(columns={
        "review_text":         "texto",
        "review_rating":       "calificacion",
        "review_datetime_utc": "fecha",
    })

    # eliminamos los nulos
    cr = cr.dropna(subset=["texto"])

    # aplicamos la funcion de polaridad a cada calificacion
    cr["polaridad"]  = cr["calificacion"].apply(obtener_polaridad)

    # agregamos el tipo de lugar y la fuente para saber de donde vienen
    cr["tipo_lugar"] = "parque"
    cr["fuente"]     = "google_maps"

    return cr


def cargar_imdb(path=IMDB_FILE, limite=1000):
    # cargamos el dataset de imdb en espanol
    imdb = pd.read_csv(path)

    # seleccionamos las columnas que vamos a usar
    imdb = imdb[["review_es", "sentimiento"]].copy()

    # quitamos los nulos
    imdb = imdb.dropna(subset=["review_es"])

    # renombramos para que tenga la misma estructura que el corpus de google maps
    imdb = imdb.rename(columns={"review_es": "texto", "sentimiento": "polaridad"})

    # limitamos a 1000 resenas para no desbalancear el corpus
    imdb = imdb.head(limite)

    # aqui no teniamos calificacion entonces la creamos a mano: negativo=1, positivo=5
    imdb["calificacion"] = imdb["polaridad"].map({"positivo": 5, "negativo": 1})

    # agregamos tipo de lugar y fuente para cumplir la estructura que necesitamos
    imdb["tipo_lugar"] = "dataset_respaldo"
    imdb["fuente"]     = "kaggle_imdb"
    imdb["fecha"]      = None

    return imdb


def unir_corpus(path_cr=CR_FILE, path_imdb=IMDB_FILE, output=OUTPUT_CSV, limite_imdb=1000):
    # definimos el orden exacto de las columnas que queremos
    columnas = ["texto", "calificacion", "polaridad", "tipo_lugar", "fuente", "fecha"]

    # cargamos y preparamos los dos corpus
    cr   = cargar_google_maps(path_cr)[columnas]
    imdb = cargar_imdb(path_imdb, limite_imdb)[columnas]

    # unimos los dos corpus y evitamos indices duplicados
    corpus_final = pd.concat([cr, imdb], ignore_index=True)

    # guardamos el resultado en csv
    corpus_final.to_csv(output, index=False, encoding="utf-8-sig")
    print("CSV generado correctamente")
    print("shape:", corpus_final.shape)

    return corpus_final


