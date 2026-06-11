import ssl
import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

warnings.filterwarnings("ignore")

# esto es para que nltk pueda descargar sus recursos sin problemas de ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# ruta del corpus limpio
SRC_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SRC_DIR, "..", "data_clean", "resenas_clean.csv")


def setup_nltk():
    # descargamos los recursos de nltk que necesitamos si no estan
    import nltk
    nltk.download("averaged_perceptron_tagger_eng", quiet=True)
    for recurso in ("tokenizers/punkt", "taggers/averaged_perceptron_tagger"):
        try:
            nltk.data.find(recurso)
        except LookupError:
            nltk.download(recurso.split("/")[-1], quiet=True)
    print("recursos de nltk listos")


def cargar_spacy(modelo="es_core_news_md"):
    import spacy, subprocess, sys
    # intentamos cargar el modelo, si no esta lo descargamos
    try:
        nlp = spacy.load(modelo)
        print(f"modelo {modelo} cargado")
    except OSError:
        print(f"modelo {modelo} no encontrado, instalando...")
        subprocess.run([sys.executable, "-m", "spacy", "download", modelo], check=True)
        nlp = spacy.load(modelo)
        print(f"modelo {modelo} instalado y cargado")
    return nlp


def pos_tagging_nltk(textos):
    from nltk.tokenize import word_tokenize
    from nltk import pos_tag

    resultados = []
    for texto in textos:
        # tokenizamos cada texto y le aplicamos el pos tagging
        tokens = word_tokenize(str(texto), preserve_line=True)
        resultados.append(pos_tag(tokens))

    print(f"nltk: {len(resultados)} resenas procesadas")
    return resultados


def pos_tagging_spacy(textos, nlp):
    resultados = []
    for texto in textos:
        doc = nlp(str(texto))
        # guardamos palabra, categoria pos, etiqueta detallada y lema
        resultados.append([(t.text, t.pos_, t.tag_, t.lemma_) for t in doc])

    print(f"spacy: {len(resultados)} resenas procesadas")
    return resultados


def comparar_nltk_spacy(texto, nlp):
    # comparamos como etiqueta cada herramienta el mismo texto
    from nltk.tokenize import word_tokenize
    from nltk import pos_tag

    tokens_nltk = word_tokenize(texto, preserve_line=True)
    pos_nltk    = pos_tag(tokens_nltk)
    doc_spacy   = nlp(texto)

    print("resena original:")
    print(f'"{texto}"\n')
    print(f"{'palabra':15} | {'nltk':10} | {'spacy pos':10} | {'spacy lema'}")
    print("-" * 60)
    for i in range(min(len(tokens_nltk), len(doc_spacy))):
        print(f"{tokens_nltk[i]:15} | {pos_nltk[i][1]:10} | "
              f"{doc_spacy[i].pos_:10} | {doc_spacy[i].lemma_}")


def graficar_distribucion_pos(doc, titulo="distribucion de etiquetas pos"):
    # contamos cuantas veces aparece cada categoria gramatical
    pos_counts = Counter(
        token.pos_ for token in doc
        if not token.is_punct and not token.is_space
    )
    pos_names  = list(pos_counts.keys())
    pos_values = list(pos_counts.values())

    # generamos el grafico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    colors  = plt.cm.Set3(range(len(pos_names)))
    bars    = ax.bar(pos_names, pos_values, color=colors, edgecolor="black", linewidth=1.5)

    # agregamos el numero encima de cada barra
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., h,
                f"{int(h)}", ha="center", va="bottom", fontweight="bold")

    ax.set_xlabel("categoria gramatical (pos)", fontsize=12, fontweight="bold")
    ax.set_ylabel("frecuencia", fontsize=12, fontweight="bold")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    plt.show()

    total = len(doc) - sum(1 for t in doc if t.is_punct or t.is_space)
    print(f"total de palabras sin puntuacion: {total}")



