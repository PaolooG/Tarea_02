# Tarea 2 - Sistemas Distribuidos 

Este proyecto implementa una arquitectura distribuida para la recolección, limpieza, análisis y cacheo eficiente de eventos de tráfico urbano, basados en datos del mapa en vivo de Waze. Todo está dockerizado, modular y documentado.

---

##  Estructura general del sistema

- **scraper/**: Extrae eventos desde Waze usando Selenium.
- **tools/**: Generador de eventos falsos realistas.
- **preprocessor/**: Limpia y normaliza los datos.
- **pig/**: Procesamiento distribuido con Apache Pig.
- **redis/**: Generador de tráfico y análisis de cacheo.
- **data/**: Entrada y salida de todos los datos CSV.
- **output/**: Resultados del procesamiento Pig.

---

##  Cómo levantar el sistema

1. **Construir la imagen personalizada**  
   ```bash
   docker-compose build
   ```

2. **Levantar todos los servicios**  
   ```bash
   docker-compose up -d
   ```

3. **Acceder al contenedor Pig (para procesamiento distribuido)**  
   ```bash
   docker exec -it pig /bin/bash
   pig pig/analisis_trafico.pig
   ```

---

## ⚙️ Ejecución de cada módulo

1. **Generar eventos sintéticos**  
   ```bash
   python tools/generador_fake_eventos.py
   ```

2. **Ejecutar preprocesador de limpieza**  
   ```bash
   python preprocessor/preprocesador.py
   ```

3. **Procesar con Pig (dentro del contenedor)**  
   ```bash
   pig pig/analisis_trafico.pig
   ```

4. **Analizar caché y rendimiento**  
   ```bash
   python redis/generador_cache_redis.py
   ```

---

## 📊 Resultados esperados

- Eventos procesados: 14.581  
- Consultas simuladas a Redis: 14.000  
- Hit rate: 99.66%  
- Tiempo promedio de respuesta: 0.0011 segundos  
- Frecuencia más alta: `Accidente:La Florida` (8.459 consultas)

---

##  Servicios incluidos en Docker

- `mongo`: Base de datos no relacional (no usada en esta entrega).
- `redis`: Caché distribuido de eventos.
- `pig`: Contenedor personalizado con Hadoop + Pig.

---

##  Archivos clave

- `eventos_raw.csv`: Datos sin procesar.
- `eventos_filtrados.csv`: Datos listos para procesamiento.
- `resultados_cache.csv`: Métricas del rendimiento del sistema.
- `frecuencia_claves.csv`: Combinaciones tipo:comuna más consultadas.
- `conteo_por_tipo`, `conteo_por_comuna`, `conteo_por_fecha`: Salidas de Pig.

---

##  Autor

**Paolo Genta**  
Alumno de Sistemas Distribuidos, 2025-1

---

##  Notas

- El uso de eventos simulados se justifica para testear rendimiento y escalabilidad.
- El scraping se realizó sobre la interfaz gráfica debido a la falta de documentación de una API oficial.
- Todos los pasos están documentados en el informe adjunto.
