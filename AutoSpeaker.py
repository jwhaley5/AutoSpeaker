import pyaudio
import wave
from scipy.io import wavfile
import matplotlib.pyplot as plt

countryRoads = "Take_Me_Home.wav"
countryNoise = "DemonstrationAudio.wav"

noiseFile = "440HzSine.wav"
noiseySignal = "noisyTrumpet.wav"
originalWav = "trumpet.wav"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2  # We will need to change this based on specifications the group decides on.
WAVE_OUTPUT_FILENAME = "output.wav"


def read_music():
    numFrames = 100
    '''actual_noise contains the noise signal useful for checking the result'''
    actual_noise = wave.open(noiseFile, 'r')
    noise = actual_noise.readframes(numFrames).hex()
    noise_list = [int(noise[i:i + 2], 16) for i in range(0, len(noise), 2)]
    actual_noise.close()

    '''Noisey Signal'''
    wf = wave.open(noiseySignal, 'r')
    print("\nNoisey Signal:", wf.getparams(), '\n')
    noisy_bytes = wf.readframes(numFrames).hex()
    wf.close()

    '''Original Wave'''
    wt = wave.open(originalWav, 'r')
    print("Original Wave:", wt.getparams(), '\n')
    wt.rewind()
    bytes_read = wt.readframes(numFrames)
    bytes_read = bytes_read.hex()
    wt.close()

    '''Uncomment the Following if you would like to see the raw pairs of hex bytes'''
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
    print("Expected output: ", noise_arr)
    print("Actual output:   ", noise_list, '\n')
    x_axis = range(numFrames * 2)
    plt.plot(x_axis, noise_arr, label='Noise-arr', color='red', marker='o', linestyle='solid', linewidth=.5,
             markersize=1)
    plt.plot(x_axis, noise_list, label='Noise_list', color='green', marker='o', linestyle='solid', linewidth=.5,
             markersize=1)
    plt.xlabel("Sample #")
    plt.ylabel("Amplitude")
    plt.legend()
    title = str(numFrames) + " Samples"
    plt.title(title)
    plt.show()

    '''Wave Output function'''
    '''Plot the 3 different Wave Files'''
    '''
    output = wave.open("output.wav", 'w')
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(44100)
    output.setnframes(numFrames)
    output.setcomptype('NONE', 'not compressed')
    output.writeframes(bytes(noise_list))
    output.close()

    numSamples = 1000
    title = str(numSamples) + " Samples"
    plt.title(title)
    plot_data(numSamples)
    '''
def plot_data(numSamples):
    x_axis = range(numSamples)
    '''Noise Signal'''
    fs, data = wavfile.read(noiseFile)
    plot_data1 = data[:numSamples]
    plt.plot(x_axis, plot_data1, label='Noise', color='green', marker='o', linestyle='solid', linewidth=.5, markersize=1)
    '''Noise + Original Signals'''
    fs, data2 = wavfile.read(noiseySignal)
    plot_data2 = data2[:numSamples]
    plt.plot(x_axis, plot_data2, label="Noise + Original", color='red', marker='o', linestyle='solid', linewidth=.5, markersize=1)
    '''Original Wave Signal'''
    fs, data3 = wavfile.read(originalWav)
    plot_data3 = data3[:numSamples]
    plt.plot(x_axis, plot_data3, label="Original Wave", color='blue', marker='o', linestyle='solid', linewidth=.5, markersize=1)
    plt.xlabel("Sample #")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()

def find_delay():
    x = [-13, -49, -56, -10, 40, 20, 20, 100, 5, 10, 5, 5, 5, 5, -13, -49, -56, -10, 40, 20, 20, 100, 5, 10, 5, 5, 5, 5]
    y = [5, 5, 5, 5, -13, -49, -56, -10, 40, 20, 20, 100, 5, 10, 5, 5, 5, 5, -13, -49, -56, -10, 40, 20, 20, 100, 5, 10]
    # correlate(x,y) is the cross correlation function
    # returns An N-dimensional array containing a subset of the discrete linear cross-correlation of in1 with in2.
    t = correlate(x, y)
    ind = 0
    max = 0
    for i in range(len(t)):
        if t[i] > max:
            ind = i
            max = t[i]
    print("max value is: ", max, " located at: ", ind)
    print(len(x))
    print(t)
    print(len(t))
    plt.plot(t)
    plt.show()


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


if __name__ == "__main__":
    #find_delay()
    read_music()
    #room_noise()

