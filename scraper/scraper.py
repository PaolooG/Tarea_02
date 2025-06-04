# scraper/scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
import csv
from datetime import datetime

ZONAS = [
    {"x_offset": 0, "y_offset": 0},
    {"x_offset": 200, "y_offset": 0},
    {"x_offset": -200, "y_offset": 0},
    {"x_offset": 0, "y_offset": 200},
    {"x_offset": 0, "y_offset": -200},
    {"x_offset": 150, "y_offset": 150},
    {"x_offset": -150, "y_offset": -150},
]

OUTPUT_JSON = "./data/eventos_raw.json"
OUTPUT_CSV = "./data/eventos_raw.csv"

def iniciar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.waze.com/es-419/live-map/")
    return driver

def presionar_entendido(driver):
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Entendido')]")
        btn.click()
        time.sleep(1)
    except:
        pass

def mover_mapa(driver, acciones, x_offset, y_offset):
    try:
        mapa = driver.find_element(By.CLASS_NAME, "leaflet-map-pane")
        acciones.drag_and_drop_by_offset(mapa, x_offset, y_offset).perform()
        time.sleep(2)
    except Exception as e:
        print(f"❌ Error al mover el mapa: {e}")

def extraer_eventos(driver, acciones):
    eventos = []
    iconos = driver.find_elements(By.CLASS_NAME, "leaflet-marker-icon")
    print(f"🔍 {len(iconos)} íconos encontrados.")
    for i in range(len(iconos)):
        try:
            iconos_actualizados = driver.find_elements(By.CLASS_NAME, "leaflet-marker-icon")
            if i >= len(iconos_actualizados):
                continue
            acciones.move_to_element(iconos_actualizados[i]).click().perform()
            time.sleep(1.5)
            popup = driver.find_element(By.CLASS_NAME, "leaflet-popup")
            texto = popup.text.strip().split("\n")
            tipo = texto[0] if len(texto) > 0 else "Desconocido"
            ubicacion = texto[1] if len(texto) > 1 else "Desconocida"
            timestamp = datetime.now().isoformat()
            comuna = "Santiago"  # Placeholder. Luego se puede inferir con coordenadas reales.
            eventos.append({
                "tipo": tipo,
                "ubicacion": ubicacion,
                "timestamp": timestamp,
                "comuna": comuna
            })
            driver.find_element(By.CLASS_NAME, "leaflet-popup-close-button").click()
        except Exception as e:
            print(f"  [{i+1}] Ignorado: {e}")
            continue
    return eventos

def guardar_json(eventos, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=4)
    print(f"✅ {len(eventos)} eventos guardados en {ruta}")

def guardar_csv(eventos, ruta):
    with open(ruta, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["tipo", "ubicacion", "timestamp", "comuna"])
        writer.writeheader()
        for evento in eventos:
            writer.writerow(evento)
    print(f"✅ {len(eventos)} eventos exportados a CSV en {ruta}")

def main():
    driver = iniciar_driver()
    acciones = ActionChains(driver)
    presionar_entendido(driver)

    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(3):
        body.send_keys(Keys.CONTROL, Keys.SUBTRACT)
        time.sleep(1)

    eventos_totales = []
    for zona in ZONAS:
        mover_mapa(driver, acciones, zona["x_offset"], zona["y_offset"])
        eventos = extraer_eventos(driver, acciones)
        eventos_totales.extend(eventos)

    driver.quit()
    guardar_json(eventos_totales, OUTPUT_JSON)
    guardar_csv(eventos_totales, OUTPUT_CSV)

if __name__ == "__main__":
    main()
