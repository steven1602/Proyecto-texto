import re
import os
import pandas as pd
from langdetect import detect

# rutas de los archivos que vamos a usar
DATA_CLEAN_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV  = os.path.join(DATA_CLEAN_DIR, "..", "data", "corpus_unificado_resenas.csv")
OUTPUT_CSV = os.path.join(DATA_CLEAN_DIR, "resenas_clean.csv")


def limpiar_texto(texto):
    # pasamos todo a minusculas
    texto = str(texto).lower()

    # quitamos urls
    texto = re.sub(r"http\S+|www\S+", "", texto)

    # quitamos emojis
    texto = re.sub(r"[\U00010000-\U0010ffff]", "", texto)

    # quitamos saltos de linea y tabs
    texto = re.sub(r"[\n\r\t]", " ", texto)

    # quitamos caracteres que no sean letras espanolas o espacios
    texto = re.sub(r"[^a-záéíóúñü\s]", "", texto)

    # quitamos espacios repetidos que quedaron
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def es_espanol(texto):
    # usamos langdetect para verificar que el texto este en espanol
    try:
        return detect(str(texto)) == "es"
    except Exception:
        return False


def limpiar_corpus(input_csv=INPUT_CSV, output_csv=OUTPUT_CSV):
    # cargamos el corpus unificado
    corpus = pd.read_csv(input_csv)

    # aplicamos la limpieza a cada texto y guardamos en una nueva columna
    corpus["texto_limpio"] = corpus["texto"].apply(limpiar_texto)

    # quitamos los nulos que quedaron
    corpus = corpus.dropna(subset=["texto_limpio"])

    # quitamos los textos que quedaron completamente vacios
    corpus = corpus[corpus["texto_limpio"] != ""]

    # esto elimina el texto donde queda solo 5 o menos caracteres
    corpus = corpus[corpus["texto_limpio"].str.len() > 5]

    # filtramos solo resenas en espanol
    corpus = corpus[corpus["texto_limpio"].apply(es_espanol)]

    # guardamos el corpus limpio
    corpus.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print("corpus limpio guardado")
    print("shape:", corpus.shape)

    return corpus



