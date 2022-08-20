from pynput.keyboard import Key, Listener
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
from scipy.io.wavfile import write
import pyaudio

mode = 1
    # 0 is recording
    # 1 is playback
fs = 44100 
seconds = 0.1 
counter = 0

def main():
    AUDIOp = AudioSegment.from_wav("pressDown.wav")
    AUDIOr = AudioSegment.from_wav("release.wav")
    
    AUDIOpn = AUDIOp.invert_phase()
    AUDIOrn = AUDIOr.invert_phase()

    def on_press(key):
        global counter
        print('{0} pressed'.format(key))
        
        if(mode == 1):
            play(AUDIOpn)

        if(mode == 0 and counter < 2):
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write('pressDown.wav', fs, myrecording)
            counter += 1

    def on_release(key):
        global counter
        print('{0} release'.format(key))
        if key == Key.esc:
            # Stop listener
            return False
        if(mode == 1):
            play(AUDIOrn)
        if(mode == 0 and counter < 2):
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  
            write('release.wav', fs, myrecording)  
            counter += 1

    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
            listener.join()

if __name__ == "__main__":
    main()