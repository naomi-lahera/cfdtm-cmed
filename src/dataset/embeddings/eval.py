# -*- coding: utf-8 -*-
import torch
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
from scipy.stats import spearmanr
import pandas as pd
import matplotlib.pyplot as plt
import umap
import numpy as np

# 1️⃣ Cargar modelo y tokenizer
model_name = "dccuchile/bert-base-spanish-wwm-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

# 2️⃣ Dataset de prueba: pares de frases médicas y score de similitud (0-5)
# Puedes sustituir por tu CSV propio
data = [
    {"text1": "El paciente tiene hipertensión arterial.", 
     "text2": "El enfermo presenta presión arterial alta.", 
     "score": 4.8},
    {"text1": "Administrar paracetamol 500 mg cada 8 horas.", 
     "text2": "Suministrar ibuprofeno 400 mg.", 
     "score": 1.5},
    {"text1": "El tumor es benigno.", 
     "text2": "El tumor es maligno.", 
     "score": 1.0},
    {"text1": "El paciente padece diabetes mellitus tipo 2.", 
     "text2": "El enfermo tiene hiperglucemia crónica.", 
     "score": 3.7},
    {"text1": "Se recomienda dieta baja en sal.", 
     "text2": "Se sugiere dieta hiposódica.", 
     "score": 4.5},
    # Añade más pares...
]

df = pd.DataFrame(data)

# 3️⃣ Función para obtener embedding de frase (usando [CLS] token)
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    # CLS token está en la posición 0
    return outputs.last_hidden_state[0][0].numpy()

# 4️⃣ Calcular embeddings y similitud
embeddings1 = np.vstack([get_embedding(t) for t in df['text1']])
embeddings2 = np.vstack([get_embedding(t) for t in df['text2']])

similarities = [1 - cosine(e1, e2) for e1, e2 in zip(embeddings1, embeddings2)]

df['similarity_cosine'] = similarities

# 5️⃣ Calcular correlación Spearman
corr, _ = spearmanr(df['score'], df['similarity_cosine'])
print(f"Correlación Spearman entre similitud humana y similitud de embeddings: {corr:.3f}")

# 6️⃣ Visualización con UMAP
# Concatenamos todas las frases y sus embeddings
all_texts = df['text1'].tolist() + df['text2'].tolist()
all_embeddings = np.vstack([embeddings1, embeddings2])

reducer = umap.UMAP(n_neighbors=5, random_state=42)
embedding_2d = reducer.fit_transform(all_embeddings)

plt.figure(figsize=(8,6))
plt.scatter(embedding_2d[:,0], embedding_2d[:,1], c='skyblue', edgecolors='k')
for i, txt in enumerate(all_texts):
    plt.annotate(txt[:25]+"..." if len(txt)>25 else txt, (embedding_2d[i,0], embedding_2d[i,1]), fontsize=8)
plt.title("Proyección UMAP de embeddings de frases médicas")
plt.show()
