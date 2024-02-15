from pydub import AudioSegment
import threading

# Función para convertir a MP3
def convert_to_mp3(file_path, output_path):
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="mp3")
    print("Conversión a MP3 completada")

# Función para convertir a WAV
def convert_to_wav(file_path, output_path):
    audio = AudioSegment.from_file(file_path, format="aiff")
    audio.export(output_path, format="wav")
    print("Conversión a WAV completada")

# Ruta del archivo original
file_path = "01 What Makes You Beautiful.aif"
# Rutas de salida
mp3_output_path = "01 What Makes You Beautiful.mp3"
wav_output_path = "01 What Makes You Beautiful.wav"

# Crear threads
thread_mp3 = threading.Thread(target=convert_to_mp3, args=(file_path, mp3_output_path))
thread_wav = threading.Thread(target=convert_to_wav, args=(file_path, wav_output_path))

# Iniciar threads
thread_mp3.start()
thread_wav.start()

# Esperar a que ambos threads terminen
thread_mp3.join()
thread_wav.join()

print("Conversión a MP3 y WAV completada")
