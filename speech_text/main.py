import pyaudio
import wave
import speech_recognition as sr
from io import BytesIO


def grabar_audio(duracion=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Grabando...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * duracion)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Grabación terminada")

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_buffer = BytesIO()
    wf = wave.open(audio_buffer, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    audio_buffer.seek(0)

    return audio_buffer


def audio_a_texto(audio_buffer):
    r = sr.Recognizer()

    with sr.AudioFile(audio_buffer) as source:
        audio = r.record(source)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender el audio")


if __name__ == "__main__":
    duration = int(input("¿Cuántos segundos quieres que dure la grabación de audio? "))
    audio_buffer = grabar_audio(duration)
    print(audio_a_texto(audio_buffer))




