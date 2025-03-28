## Primer parcial
### Programa de procesamiento de imágenes satelitales
Judith Mª. Salas García

Este script simula un centro de procesamiento digital de imágenes recibidas desde satélites, implementando el patrón **Productor-Consumidor** con programación paralela utilizando el módulo `multiprocessing` de Python.

### Objetivo

- Simular la **recepción asíncrona** de imágenes satelitales.
- Procesarlas en paralelo mediante **analistas automáticos**.
- Garantizar que **no se pierda ninguna imagen**, incluso bajo carga alta.
- Sincronizar los procesos consumidores para que **comiencen todos al mismo tiempo**.
- Medir y mostrar el tiempo que tarda cada imagen en ser procesada.

---

### Tecnologías utilizadas

- Python 3.8 o superior
- `multiprocessing` (módulo estándar)

---

### Archivos del proyecto

- `procesamiento_satelital.py` → Código principal con el sistema concurrente.
- `README.md` → Instrucciones para ejecutar y entender el proyecto.

---

### ¿Cómo ejecutar el script?

1. Abre una terminal.
2. Navega a la carpeta donde esté guardado el archivo `procesamiento_satelital.py`.
3. Ejecuta el script con:

```bash
python procesamiento_satelital.py
