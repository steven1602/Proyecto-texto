import os
import warnings
import pandas as pd
from collections import Counter

warnings.filterwarnings("ignore")

# ruta del corpus limpio
SRC_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SRC_DIR, "..", "data_clean", "resenas_clean.csv")


def estadisticas_basicas(corpus):
    corpus = corpus.copy()

    # contamos cuantas palabras tiene cada resena
    corpus["cantidad_palabras"]   = corpus["texto_limpio"].apply(lambda x: len(str(x).split()))

    # contamos cuantos caracteres tiene cada resena
    corpus["cantidad_caracteres"] = corpus["texto_limpio"].apply(len)

    # sacamos el resumen estadistico de esas dos columnas
    resumen = corpus[["cantidad_palabras", "cantidad_caracteres"]].describe().round(2)

    return corpus, resumen


def palabras_frecuentes(corpus, n=15):
    # unimos todos los textos del corpus en uno solo
    palabras = " ".join(corpus["texto_limpio"].astype(str)).split()

    # counter cuenta cuantas veces aparece cada palabra
    frecuencia = Counter(palabras)

    # devolvemos las n palabras mas repetidas
    return pd.DataFrame(frecuencia.most_common(n), columns=["palabra", "frecuencia"])


def contar_pos(documentos):
    # recorremos cada documento y contamos las etiquetas pos
    contador = Counter()
    for doc in documentos:
        for token in doc:
            if not token.is_space:
                contador[token.pos_] += 1
    return contador


def distribucion_pos(corpus):
    # contamos las etiquetas pos de todo el corpus
    pos_counter  = contar_pos(corpus["spacy_doc"])
    total_tokens = sum(pos_counter.values())

    # convertimos el contador a dataframe y ordenamos de mayor a menor
    df = pd.DataFrame(
        list(pos_counter.items()),
        columns=["categoria_pos", "cantidad"]
    ).sort_values("cantidad", ascending=False)

    # agregamos el porcentaje de cada categoria
    df["porcentaje"] = round((df["cantidad"] / total_tokens) * 100, 2)

    return df


def comparacion_pos_polaridad(corpus, categorias=None):
    if categorias is None:
        categorias = ["NOUN", "VERB", "ADJ", "ADV", "PRON"]

    # filtramos por resenas positivas y negativas
    positivas = corpus[corpus["polaridad"] == "positivo"]
    negativas = corpus[corpus["polaridad"] == "negativo"]

    # llamamos a la funcion pasandole los documentos de cada grupo
    pos_positivas = contar_pos(positivas["spacy_doc"])
    pos_negativas = contar_pos(negativas["spacy_doc"])

    return pd.DataFrame({
        "POS":       categorias,
        "Positivas": [pos_positivas[c] for c in categorias],
        "Negativas": [pos_negativas[c] for c in categorias],
    })


def procesar_corpus_morfologico(input_csv=INPUT_CSV, nlp=None):
    import spacy

    # cargamos el corpus limpio
    corpus = pd.read_csv(input_csv)

    # si no nos pasan el modelo lo cargamos aqui
    if nlp is None:
        nlp = spacy.load("es_core_news_md")

    # aplicamos el pipeline de spacy a cada resena
    corpus["spacy_doc"] = corpus["texto_limpio"].astype(str).apply(nlp)

    # sacamos las estadisticas y distribuciones
    corpus, resumen   = estadisticas_basicas(corpus)
    df_pos            = distribucion_pos(corpus)
    df_comparacion    = comparacion_pos_polaridad(corpus)

    return corpus, resumen, df_pos, df_comparacion


