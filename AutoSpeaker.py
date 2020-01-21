import pyaudio
import wave
from scipy.io import wavfile
import matplotlib.pyplot as plt

countryRoads = "Take_Me_Home.wav"
countryNoise = "DemonstrationAudio.wav"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2  # We will need to change this based on specifications for autocorrelation
WAVE_OUTPUT_FILENAME = "output.wav"

def readMusic():
    fs, data = wavfile.read('440HzSine.wav')
    print(fs)
    plt.plot(data)
    plt.ylabel("16-bit PCM Sample")

    
    sinewav = wave.open("440HzSine.wav", 'r')
    sines = sinewav.readframes(48075).hex()
    sinlist = [int(sines[i:i + 2],16) for i in range(0, len(sines), 2)]
    sinewav.close()
    wf = wave.open('noisyTrumpet.wav', 'r')
    print(wf.getparams())
    noisy_bytes = wf.readframes(48075).hex()
    wf.close()
    wt = wave.open('trumpet.wav', 'r')
    print(wt.getparams())
    wt.rewind()
    bytes_read = wt.readframes(48075)
    bytes_read = bytes_read.hex()
    #print("bytes containing the trumpet with added noise: ", noisy_bytes)
    #print("bytes containing the trumpet with no noise:    ", bytes_read)

    n = 2
    noisy_list = [int(noisy_bytes[i:i + n], 16) for i in range(0, len(noisy_bytes), n)]
    clean_list = [int(bytes_read[i:i + n], 16) for i in range(0, len(bytes_read), n)]
    noise_arr = []
    for i in range(len(clean_list)):
        num = noisy_list[i] - clean_list[i]
        if num < 0:
            num = num + 255
        noise_arr.append(num)
    print(noise_arr)
    print(sinlist)
    plt.show()
    wt.close()




def room_noise():
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

if __name__ == "__main__" :
    readMusic()

