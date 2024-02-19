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
    print(f"Conversión a MP3 completada. Tamaño: {get_file_size(output_path)} bytes. Comenzó en t={elapsed_start:.2f}s y terminó en t={elapsed_end:.2f}s")

def convert_to_wav(file_path, output_path, start_time):
    local_start_time = time.time()
    elapsed_start = local_start_time - start_time
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="wav")
    local_end_time = time.time()
    elapsed_end = local_end_time - start_time
    print(f"Conversión a WAV completada. Tamaño: {get_file_size(output_path)} bytes. Comenzó en t={elapsed_start:.2f}s y terminó en t={elapsed_end:.2f}s")

def convert_to_m4a(file_path, output_path, start_time):
    local_start_time = time.time()
    elapsed_start = local_start_time - start_time
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="ipod", codec="aac")
    local_end_time = time.time()
    elapsed_end = local_end_time - start_time
    print(f"Conversión a M4A completada. Tamaño: {get_file_size(output_path)} bytes. Comenzó en t={elapsed_start:.2f}s y terminó en t={elapsed_end:.2f}s")

def convert_file_to_format(file_path, output_format, start_time):
    base_name = os.path.splitext(file_path)[0]
    output_path = f"{base_name}.{output_format}"
    if output_format == "mp3":
        convert_to_mp3(file_path, output_path, start_time)
    elif output_format == "wav":
        convert_to_wav(file_path, output_path, start_time)
    elif output_format == "m4a":
        convert_to_m4a(file_path, output_path, start_time)

def process_directory(directory_path, output_format, start_time, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.aif'):
                    file_path = os.path.join(root, file)
                    executor.submit(convert_file_to_format, file_path, output_format, start_time)


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
    
    parser = argparse.ArgumentParser(description='Disc Music Compressor: Convierte archivos a MP3, WAV y M4A')
    parser.add_argument('-f', '--file', help='El nombre del archivo o directorio a convertir', required=True)
    parser.add_argument('-e', '--extension', help='Formato de salida para la conversión (requerido solo para directorios)')
    
    args = parser.parse_args()

    if os.path.isdir(args.file):
        if not args.extension or args.extension not in ['mp3', 'wav', 'm4a']:
            print("Error: Debes especificar un formato de salida válido (-e mp3, wav, m4a) para procesar un directorio.")
        else:
            process_directory(args.file, args.extension, start_time)
    elif os.path.isfile(args.file):
        if args.file.lower().endswith('.aif'):
            process_single_file(args.file, start_time)  
        else:
            print("Error: El archivo especificado no es un archivo .aif")
    else:
        print("El archivo o directorio especificado no existe.")
