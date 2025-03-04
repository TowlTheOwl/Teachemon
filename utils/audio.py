import sounddevice as sd
import wave
import pyaudio
from piper import PiperVoice

wav_file = "speech.wav"
p = pyaudio.PyAudio()
voice = PiperVoice.load("en_US-norman-medium.onnx")

def playAudio(audio):
    wf = wave.open(audio)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getchannels(), rate=wf.getframerate(), output=True)
    while len(data := wf.readframes(1024)):
        stream.write(data)
    stream.close()
    print("Audio played")

def createAudio(text):
    with wave.open("speech.wav", "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        voice.synthesize(text, wav_file)
        print("Audio created")