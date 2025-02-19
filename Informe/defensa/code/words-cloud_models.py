import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Definir las palabras con sus ponderaciones (frecuencias)
palabras = {
    "DETM": 20,
    "CFDTM": 20,
    "NetDTM": 10,
    "NetDTM++": 10,
    "ANTM": 15,
    "DSNTM": 15, "NDF-TM": 10
}

# Crear la nube de palabras
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="plasma"
).generate_from_frequencies(palabras)

# Mostrar la nube de palabras
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
