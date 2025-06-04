# preprocessor/preprocesador.py

import pandas as pd
import os
import re
from datetime import datetime, timedelta

INPUT_CSV = "./data/eventos_raw.csv"
OUTPUT_CSV = "./data/eventos_filtrados.csv"

# Diccionario de normalización de tipos de eventos
NORMALIZACION_TIPOS = {
    "control policial": "Policía",
    "policía en camino": "Policía",
    "policía": "Policía",
    "accidente": "Accidente",
    "atasco": "Atasco",
    "corte de vía": "Corte",
    "corte": "Corte",
    "bache": "Bache",
    "vehículo detenido": "Detención",
    "vehiculo detenido": "Detención",
}

def normalizar_tipo(texto):
    texto = texto.lower().strip()
    for patron, tipo_unificado in NORMALIZACION_TIPOS.items():
        if patron in texto:
            return tipo_unificado
    return texto.capitalize()

def cargar_datos(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    return pd.read_csv(path)

def limpiar_y_filtrar(df):
    # Quitar eventos sin datos esenciales
    df = df.dropna(subset=["tipo", "ubicacion", "timestamp", "comuna"])
    
    # Normalizar tipo
    df["tipo"] = df["tipo"].apply(normalizar_tipo)

    # Parsear timestamp a datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df.dropna(subset=["timestamp"])
    
    return df

def eliminar_duplicados_aproximados(df):
    # Ordenar por comuna, tipo y timestamp
    df = df.sort_values(by=["comuna", "tipo", "timestamp"])

    # Agrupar eventos similares en una misma comuna y tipo, dentro de 5 minutos
    resultado = []
    ultima_firma = {}

    for _, row in df.iterrows():
        clave = (row["comuna"], row["tipo"])
        tiempo = row["timestamp"]

        if clave not in ultima_firma or tiempo - ultima_firma[clave] > timedelta(minutes=5):
            resultado.append(row)
            ultima_firma[clave] = tiempo

    return pd.DataFrame(resultado)

def guardar_datos(df, path):
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"✅ Archivo limpio guardado en: {path} ({len(df)} eventos)")

def main():
    print("🧹 Iniciando limpieza de eventos...")
    df = cargar_datos(INPUT_CSV)
    df = limpiar_y_filtrar(df)
    df = eliminar_duplicados_aproximados(df)
    guardar_datos(df, OUTPUT_CSV)

if __name__ == "__main__":
    main()
