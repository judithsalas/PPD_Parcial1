import multiprocessing
import time
import random
from datetime import datetime


def receptor_imagenes(queue, num_imagenes):
    for i in range(1, num_imagenes + 1):
        time.sleep(random.uniform(0.1, 1.5))  # Simula llegada variable
        imagen = f"imagen_{i}"
        queue.put(imagen)
        print(f"[{timestamp()}] [RECEPCIÓN] Imagen recibida: {imagen}")
    print(f"[{timestamp()}] [RECEPCIÓN] Finalizó la recepción de imágenes.")


def procesador_imagenes(queue, barrera, identificador):
    print(f"[{timestamp()}] [ANÁLISIS-{identificador}] Esperando en la barrera...")
    barrera.wait()
    print(f"[{timestamp()}] [ANÁLISIS-{identificador}] Iniciando procesamiento.")

    while True:
        imagen = queue.get()
        if imagen == "FIN":
            print(f"[{timestamp()}] [ANÁLISIS-{identificador}] Proceso finalizado.")
            break

        inicio = time.time()
        print(f"[{timestamp()}] [ANÁLISIS-{identificador}] Procesando {imagen}...")
        time.sleep(random.uniform(2, 5))  # Simula procesamiento costoso
        fin = time.time()

        print(f"[{timestamp()}] [ANÁLISIS-{identificador}] Imagen procesada: {imagen} "
              f"({fin - inicio:.2f} s)")


def timestamp():
    """Devuelve hora actual como string HH:MM:SS"""
    return datetime.now().strftime("%H:%M:%S")


if __name__ == "__main__":
    multiprocessing.freeze_support()

    # Puedes ajustar el tamaño máximo del buffer si lo deseas
    buffer = multiprocessing.Queue(maxsize=10)

    NUM_IMAGENES = 20
    NUM_ANALIZADORES = 3
    barrera = multiprocessing.Barrier(NUM_ANALIZADORES)

    productor = multiprocessing.Process(target=receptor_imagenes, args=(buffer, NUM_IMAGENES))
    consumidores = [
        multiprocessing.Process(target=procesador_imagenes, args=(buffer, barrera, i + 1))
        for i in range(NUM_ANALIZADORES)
    ]

    try:
        productor.start()
        for c in consumidores:
            c.start()

        productor.join()

        for _ in consumidores:
            buffer.put("FIN")

        for c in consumidores:
            c.join()

        print(f"[{timestamp()}] Sistema finalizado correctamente.")

    except KeyboardInterrupt:
        print("\n Interrupción del sistema detectada. Cerrando procesos...")
        productor.terminate()
        for c in consumidores:
            c.terminate()
