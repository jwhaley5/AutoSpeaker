import pyaudio
import wave

countryRoads = "Take_Me_Home.mp3"
countryNoise = "DemonstrationAudio.wav"

# Auto-correlate the two audio files

#

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2  # We will need to change this based on specifications for autocorrelation
WAVE_OUTPUT_FILENAME = "output.wav"

roomInput = pyaudio.PyAudio()

stream = roomInput.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    print(i, "samples recorded")

print("* done recording")

stream.stop_stream()
stream.close()
roomInput.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(roomInput.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
