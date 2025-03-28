import multiprocessing
import time
import random



# FUNCIÓN PRODUCTOR

def receptor_imagenes(queue, num_imagenes):
    """
    Simula la llegada de imágenes desde satélites y las añade a la cola compartida.
    La llegada es irregular, simulando condiciones reales de transmisión.
    """
    for i in range(1, num_imagenes + 1):
        time.sleep(random.uniform(0.1, 1.5))  # Espera aleatoria entre imágenes
        imagen = f"imagen_{i}"  # Imagen identificada por número secuencial
        queue.put(imagen)       # Inserta imagen en la cola
        print(f"[RECEPCIÓN] Imagen recibida: {imagen}")
    
    print("[RECEPCIÓN] Finalizó la recepción de imágenes.")



# FUNCIÓN CONSUMIDOR

def procesador_imagenes(queue, barrera, identificador):
    """
    Procesa las imágenes recibidas, simulando un análisis complejo.
    Espera a que todos los consumidores estén listos antes de comenzar (barrera).
    """
    print(f"[ANÁLISIS-{identificador}] Esperando en la barrera...")
    barrera.wait()  # Sincronización: todos los consumidores comienzan juntos
    print(f"[ANÁLISIS-{identificador}] Iniciando procesamiento.")

    while True:
        imagen = queue.get()  # Toma una imagen de la cola
        if imagen == "FIN":   # Señal especial para detener el proceso
            print(f"[ANÁLISIS-{identificador}] Proceso finalizado.")
            break
        
        print(f"[ANÁLISIS-{identificador}] Procesando {imagen}...")
        time.sleep(random.uniform(2, 5))  # Simula análisis costoso
        print(f"[ANÁLISIS-{identificador}] Imagen procesada: {imagen}")



# BLOQUE PRINCIPAL

if __name__ == "__main__":
    multiprocessing.freeze_support()  

    # Cola segura para comunicación entre procesos (buffer compartido)
    buffer = multiprocessing.Queue()

    # Configuración del sistema
    NUM_IMAGENES = 20           # Total de imágenes a recibir
    NUM_ANALIZADORES = 3        # Cantidad de procesos consumidores

    # Barrera de sincronización: todos los consumidores deben estar listos antes de comenzar
    barrera = multiprocessing.Barrier(NUM_ANALIZADORES)

    # Proceso productor: simula la llegada de imágenes
    productor = multiprocessing.Process(target=receptor_imagenes, args=(buffer, NUM_IMAGENES))

    # Procesos consumidores: simulan el análisis de las imágenes
    consumidores = [
        multiprocessing.Process(target=procesador_imagenes, args=(buffer, barrera, i+1))
        for i in range(NUM_ANALIZADORES)
    ]

    # Iniciar productor y consumidores
    productor.start()
    for c in consumidores:
        c.start()

    # Espera a que el productor termine de recibir todas las imágenes
    productor.join()

    # Envía la señal de parada ("FIN") a cada consumidor
    for _ in consumidores:
        buffer.put("FIN")

    # Espera a que todos los consumidores finalicen su trabajo
    for c in consumidores:
        c.join()

    print("Sistema finalizado correctamente.")
