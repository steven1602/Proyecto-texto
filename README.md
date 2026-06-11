# Análisis Morfosintáctico de Reseñas Turísticas de Costa Rica
### Aplicando POS Tagging con NLTK y spaCy

**Curso:** Minería de Textos · Colegio Universitario de Cartago (CUC)  
**Profesor:** Osval Gonzalez Chaves  
**Equipo:** *steven vindas*

---

## Descripción

Este proyecto aplica técnicas de Procesamiento de Lenguaje Natural (PLN) para analizar la estructura morfosintáctica de reseñas turísticas de Costa Rica. Mediante POS Tagging con NLTK y spaCy se identifican patrones gramaticales que distinguen reseñas positivas de negativas.

El corpus combina **reseñas reales de Google Maps** (parques nacionales de Costa Rica) con un **dataset de respaldo en español** (IMDB traducido), totalizando 1,008 reseñas procesadas.

---

## Estructura del Repositorio

```
proyecto_pos/
│
├── notebooks/
│   ├── 01_union_corpus.ipynb        # Unión de fuentes (Google Maps + IMDB)
│   ├── 02_clean_resenas.ipynb       # Limpieza y normalización del texto
│   ├── 03_POS_tagging.ipynb         # POS Tagging con NLTK y spaCy + comparación
│   ├── 04_analisis_morfologico.ipynb# Métricas morfológicas y análisis por polaridad
│   └── 05_visualizaciones_pos.ipynb # Gráficos con matplotlib
│
├── src/
│   ├── pos_tagging.py               # Funciones de etiquetado POS
│   ├── metrics.py                   # Cálculo de métricas morfológicas
│   └── visualizations.py            # Funciones de visualización Plotly
│
├── dashboard/
│   └── app.py                       # Dashboard interactivo con Plotly Dash
│
├── data/
│   └── resenas_clean.csv            # Corpus limpio (generado por los notebooks)
│
├── requirements.txt
├── USO_DE_IA.md
└── README.md
```

---

## Corpus

| Fuente | Registros | Tipo |
|--------|-----------|------|
| Google Maps (Outscraper) | ~376 reseñas | Parques nacionales CR |
| Kaggle IMDB en español | ~1,000 reseñas | Dataset de respaldo |
| **Total procesado** | **1,008 reseñas** | Después de limpieza |

---

## Pipeline de Análisis

1. **Unión del corpus** → `01_union_corpus.ipynb`
2. **Limpieza y normalización** → `02_clean_resenas.ipynb`
3. **POS Tagging** (NLTK + spaCy) → `03_POS_tagging.ipynb`
4. **Análisis morfológico** → `04_analisis_morfologico.ipynb`
5. **Visualizaciones** → `05_visualizaciones_pos.ipynb`
6. **Dashboard interactivo** → `dashboard/app.py`

---




```



---

## Principales Hallazgos

- Las reseñas **positivas** presentan mayor densidad de adjetivos que las negativas.
- El ratio sustantivos/verbos es similar entre polaridades, indicando estructuras gramaticales comparables.
- **spaCy** supera a NLTK para texto en español: NLTK clasifica incorrectamente preposiciones y conjunciones al estar orientado al inglés (Penn Treebank).
- Las reseñas positivas tienden a ser más largas en promedio.

---

## Herramientas Utilizadas

| Herramienta | Uso |
|-------------|-----|
| spaCy `es_core_news_md` | Pipeline principal de POS Tagging |
| NLTK `pos_tag` | Comparación de sistemas de etiquetas |
| pandas | Manipulación del corpus |
| Plotly Dash | Dashboard interactivo |
| Outscraper | Recolección de reseñas de Google Maps |