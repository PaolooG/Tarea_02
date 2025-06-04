import pandas as pd
import redis
import json
import random
import time
import numpy as np
from collections import defaultdict
import csv

CSV_INPUT = "./data/eventos_filtrados.csv"
ITERACIONES = 14000
DISTRIBUCION = "zipf"  # o "uniforme"
TTL_SEGUNDOS = 60

def cargar_eventos():
    return pd.read_csv(CSV_INPUT)

def conectar_redis():
    return redis.Redis(host="localhost", port=6379, decode_responses=True)

def generar_clave(tipo, comuna):
    return f"{tipo}:{comuna}"

def simular_trafico(df, r):
    tipos = df["tipo"].unique()
    comunas = df["comuna"].unique()
    combinaciones = [(t, c) for t in tipos for c in comunas]

    hits = 0
    misses = 0
    duraciones = []
    frecuencia = defaultdict(int)

    for i in range(ITERACIONES):
        if DISTRIBUCION == "uniforme":
            tipo, comuna = random.choice(combinaciones)
        elif DISTRIBUCION == "zipf":
            idx = min(np.random.zipf(2), len(combinaciones)) - 1
            tipo, comuna = combinaciones[idx]
        else:
            raise ValueError("Distribución no válida")

        clave = generar_clave(tipo, comuna)
        inicio = time.time()

        if r.exists(clave):
            _ = json.loads(r.get(clave))
            hits += 1
        else:
            resultados = df[(df["tipo"] == tipo) & (df["comuna"] == comuna)]
            data = resultados.to_dict(orient="records")
            r.set(clave, json.dumps(data))
            r.expire(clave, TTL_SEGUNDOS)
            misses += 1

        duracion = time.time() - inicio
        duraciones.append(duracion)
        frecuencia[clave] += 1

    return {
        "total": ITERACIONES,
        "hits": hits,
        "misses": misses,
        "hit_rate": hits / ITERACIONES * 100,
        "avg_time": sum(duraciones) / ITERACIONES,
        "frecuencia": dict(frecuencia)
    }

def guardar_metricas(resultados, ruta="data/resultados_cache.csv"):
    with open(ruta, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Métrica", "Valor"])
        writer.writerow(["Consultas totales", resultados["total"]])
        writer.writerow(["Hits", resultados["hits"]])
        writer.writerow(["Misses", resultados["misses"]])
        writer.writerow(["Hit rate (%)", f"{resultados['hit_rate']:.2f}"])
        writer.writerow(["Tiempo promedio (s)", f"{resultados['avg_time']:.4f}"])
    print(f"📁 Métricas guardadas en {ruta}")

def guardar_frecuencia(frecuencia, ruta="data/frecuencia_claves.csv"):
    with open(ruta, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Clave", "Frecuencia"])
        for clave, frec in frecuencia.items():
            writer.writerow([clave, frec])
    print(f"📁 Frecuencia guardada en {ruta}")

def main():
    print("🚦 Generando tráfico simulado con Redis...")
    df = cargar_eventos()
    r = conectar_redis()
    r.flushdb()

    resultados = simular_trafico(df, r)

    print("\n📊 Resultados:")
    print(f" - Consultas totales: {resultados['total']}")
    print(f" - Hits: {resultados['hits']}")
    print(f" - Misses: {resultados['misses']}")
    print(f" - Hit rate: {resultados['hit_rate']:.2f}%")
    print(f" - Tiempo promedio por consulta: {resultados['avg_time']:.4f} segundos")

    guardar_metricas(resultados)
    guardar_frecuencia(resultados["frecuencia"])

if __name__ == "__main__":
    main()
