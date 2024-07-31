import yt_dlp
import os
import subprocess
import sys

def convertir_a_mp3(input_file, output_file):
    try:
        # Ruta del ejecutable de FFmpeg (debe estar en la carpeta bin dentro del directorio actual)
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffmpeg.exe')
        subprocess.run([
            ffmpeg_path, '-i', input_file, '-q:a', '0', '-map', 'a', output_file
        ], check=True)
        print(f'Archivo convertido a MP3: {output_file}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error al convertir el archivo: {e}')
        return False

def descargar_audio(url, path='.'):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_title = info_dict.get('title', 'audio')
            # Busca el archivo descargado
            downloaded_file = os.path.join(path, f'{audio_title}.webm')
            if os.path.exists(downloaded_file):
                mp3_file = os.path.join(path, f'{audio_title}.mp3')
                if convertir_a_mp3(downloaded_file, mp3_file):
                    os.remove(downloaded_file)  # Elimina el archivo original después de convertir
                    return True
            else:
                print('El archivo webm no se encontró.')
            return False
    except Exception as e:
        print(f'Error al descargar el audio: {e}')
        return False

def main():
    while True:
        url = input('Introduce el enlace del video de YouTube (o "salir" para terminar): ')
        if url.lower() == 'salir':
            break
        path = input('Introduce el directorio donde quieres guardar el audio (presiona Enter para usar el directorio actual): ')
        path = path if path else '.'
        if not os.path.exists(path):
            print('El directorio no existe, se usará el directorio actual.')
            path = '.'
        
        if descargar_audio(url, path):
            continue
        else:
            print('Introduce un nuevo enlace.')

if __name__ == "__main__":
    main()
