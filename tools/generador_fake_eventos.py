import csv
import random
from datetime import datetime, timedelta

TIPOS_EVENTO = ["Policía", "Accidente", "Atasco", "Corte", "Bache", "Detención"]
COMUNAS = ["Santiago", "Maipú", "Ñuñoa", "Providencia", "Puente Alto", "La Florida", "Las Condes", "Macul"]

def generar_eventos(n):
    eventos = []
    base_time = datetime.now() - timedelta(days=5)

    for _ in range(n):
        tipo = random.choices(TIPOS_EVENTO, weights=[0.3, 0.25, 0.2, 0.15, 0.05, 0.05])[0]
        comuna = random.choice(COMUNAS)
        ubicacion = f"Calle falsa #{random.randint(1, 3000)}"
        timestamp = (base_time + timedelta(seconds=random.randint(0, 432000))).isoformat()

        eventos.append({
            "tipo": tipo,
            "ubicacion": ubicacion,
            "timestamp": timestamp,
            "comuna": comuna
        })

    return eventos

def guardar_csv(eventos, ruta):
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["tipo", "ubicacion", "timestamp", "comuna"])
        writer.writeheader()
        writer.writerows(eventos)

if __name__ == "__main__":
    eventos = generar_eventos(20000)
    guardar_csv(eventos, "./data/eventos_fake.csv")
    print(f"✅ Generados {len(eventos)} eventos falsos realistas.")
