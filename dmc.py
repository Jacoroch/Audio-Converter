import argparse
from pydub import AudioSegment
import threading
import os
from concurrent.futures import ThreadPoolExecutor
import time

def get_file_size(file_path):
    return os.path.getsize(file_path)

def convert_to_mp3(file_path, output_path, start_time):
    local_start_time = time.time()
    elapsed_start = local_start_time - start_time
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="mp3")
    local_end_time = time.time()
    elapsed_end = local_end_time - start_time
    print(f"Conversión a MP3 completada. Tamaño: {get_file_size(output_path)} bytes. Comenzó en t={elapsed_start:.3f}s y terminó en t={elapsed_end:.3f}s")

def convert_to_wav(file_path, output_path, start_time):
    local_start_time = time.time()
    elapsed_start = local_start_time - start_time
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="wav")
    local_end_time = time.time()
    elapsed_end = local_end_time - start_time
    print(f"Conversión a WAV completada. Tamaño: {get_file_size(output_path)} bytes. Comenzó en t={elapsed_start:.3f}s y terminó en t={elapsed_end:.3f}s")

def convert_to_m4a(file_path, output_path, start_time):
    local_start_time = time.time()
    elapsed_start = local_start_time - start_time
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="ipod", codec="aac")
    local_end_time = time.time()
    elapsed_end = local_end_time - start_time
    print(f"Conversión a M4A completada. Tamaño: {get_file_size(output_path)} bytes. Comenzó en t={elapsed_start:.3f}s y terminó en t={elapsed_end:.3f}s")

def process_directory(directory_path, output_format, start_time, max_workers=13):
    print("workers: "+ str(max_workers))
    # Crear el nombre de la nueva carpeta añadiendo el formato al nombre original
    new_directory_name = f"{directory_path} [{output_format}]"
    # Crear la carpeta si no existe
    if not os.path.exists(new_directory_name):
        os.makedirs(new_directory_name)
    
    #Crear los hilos para convertir los archivos en paralelo
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.aif'):
                    file_path = os.path.join(root, file)
                    # Construir la ruta de salida en la nueva carpeta
                    base_name = os.path.splitext(file)[0]
                    output_path = os.path.join(new_directory_name, f"{base_name}.{output_format}")
                    # Enviar la ruta de salida correcta junto con el formato y el tiempo de inicio
                    executor.submit(convert_file_to_format, file_path, output_path, output_format, start_time)

def convert_file_to_format(file_path, output_path, output_format, start_time):
    if output_format == "mp3":
        convert_to_mp3(file_path, output_path, start_time)
    elif output_format == "wav":
        convert_to_wav(file_path, output_path, start_time)
    elif output_format == "m4a":
        convert_to_m4a(file_path, output_path, start_time)

def process_single_file(file_path, start_time):
    #nombre de los archivos de salida
    base_name = os.path.splitext(file_path)[0]
    mp3_output_path = f"{base_name}.mp3"
    wav_output_path = f"{base_name}.wav"
    m4a_output_path = f"{base_name}.m4a"

    threads = [
        threading.Thread(target=convert_to_m4a, args=(file_path, m4a_output_path, start_time)),
        threading.Thread(target=convert_to_mp3, args=(file_path, mp3_output_path, start_time)),
        threading.Thread(target=convert_to_wav, args=(file_path, wav_output_path, start_time))
    ]
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    print("Conversión completada. Elija el formato que desea conservar (mp3, wav, m4a):")
    choice = input().lower()
    while choice != "mp3" and choice != "wav" and choice != "m4a":
        print("Escribe un formato válido: (mp3, wav, m4a)")
        choice = input().lower()  # Solicitar nuevamente la entrada del usuario antes de mostrar el mensaje de formato elegido
        print("Formato elegido: " + choice)
        
    # Eliminar archivos no elegidos
    if choice != "mp3":
        os.remove(mp3_output_path)
    if choice != "wav":
        os.remove(wav_output_path)
    if choice != "m4a":
        os.remove(m4a_output_path)

    print(f"El archivo en formato {choice} ha sido conservado.")

if __name__ == "__main__":
    start_time = time.time()
    exit_status = 0  

    try:
        parser = argparse.ArgumentParser(description='Disc Music Compressor')
        parser.add_argument('-f', '--file', required=True)
        parser.add_argument('-e', '--extension', default='')

        args = parser.parse_args()

        if os.path.isdir(args.file):
            if not args.extension or args.extension not in ['mp3', 'wav', 'm4a']:
                print("Error: Debes especificar un formato de salida válido (-e mp3, wav, m4a) para procesar una carpeta.")
                exit_status = 1  
            else:
                process_directory(args.file, args.extension, start_time)
        elif os.path.isfile(args.file):
            if args.file.lower().endswith('.aif'):
                process_single_file(args.file, start_time)
            else:
                print("Error: El archivo especificado no es un archivo .aif")
                exit_status = 1  
        else:
            print("El archivo o directorio especificado no existe.")
            exit_status = 1  
    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")
        exit_status = 1  
    finally:
        print("Estado de salida del proceso:"+ str(exit_status))
        
#python dmc.py -e wav -f "Up All Night"
#python dmc.py -f "01 What Makes You Beautiful.aif"
