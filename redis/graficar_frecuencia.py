import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/frecuencia_claves.csv")

# Opcional: ordenar por frecuencia
df = df.sort_values(by="Frecuencia", ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.bar(df["Clave"], df["Frecuencia"], color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 combinaciones más consultadas (tipo:comuna)")
plt.xlabel("Clave")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("data/frecuencia_top10.png")
plt.show()
