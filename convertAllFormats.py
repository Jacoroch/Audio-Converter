import subprocess
import re
import os

def ejecutar_y_registrar(formato, numero_de_ejecuciones, archivo_o_carpeta):
    tiempos_de_ejecucion = []
    num_workers = "desconocido"  # Valor predeterminado

    for i in range(numero_de_ejecuciones):
        comando = f"python dmc.py -e {formato} -f \"{archivo_o_carpeta}\""
        resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
        salida = resultado.stdout

        # Intentar extraer el número de workers solo en la primera ejecución
        if i == 0:
            match_workers = re.search(r"workers: (\d+)", salida)
            if match_workers:
                num_workers = match_workers.group(1)

        # Extraer el tiempo final de ejecución utilizando expresiones regulares
        matches = re.findall(r"t=(\d+\.\d{1,3})s", salida)
        if matches:
            tiempo_final = float(matches[-1])
            tiempos_de_ejecucion.append(tiempo_final)
            print(f"Ejecución {i+1}: Tiempo final = {tiempo_final}s")

    # Calcular el promedio, el menor y el mayor tiempo de ejecución
    promedio = sum(tiempos_de_ejecucion) / len(tiempos_de_ejecucion) if tiempos_de_ejecucion else 0
    menor_tiempo = min(tiempos_de_ejecucion) if tiempos_de_ejecucion else 0
    mayor_tiempo = max(tiempos_de_ejecucion) if tiempos_de_ejecucion else 0

    # Crear la carpeta "workers" si no existe
    carpeta_salida = "workers"
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Escribir los resultados en un archivo dentro de la carpeta "workers"
    nombre_archivo = os.path.join(carpeta_salida, f"{formato} {num_workers} workers.txt")
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(f"{formato.upper()}\n")
        for i, tiempo in enumerate(tiempos_de_ejecucion, start=1):
            archivo.write(f"Ejecución {i}: Tiempo final = {tiempo:.3f}s\n")
        archivo.write(f"Promedio de tiempo de ejecución: {promedio:.3f}s\n")
        archivo.write(f"Menor tiempo de ejecución: {menor_tiempo:.3f}s\n")
        archivo.write(f"Mayor tiempo de ejecución: {mayor_tiempo:.3f}s\n")

# Configuración inicial
numero_de_ejecuciones = 20
formatos = ["wav", "mp3", "m4a"]
archivo_o_carpeta = "Up All Night"

for formato in formatos:
    ejecutar_y_registrar(formato, numero_de_ejecuciones, archivo_o_carpeta)
