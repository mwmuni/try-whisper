
# # List all audio devices

# import pyaudio
# p = pyaudio.PyAudio()
# devices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
# names = [(d['index'], d['name']) for d in devices]

# for name in names:
#     print(name)

# exit()

#! Yeti mic is index 2

from pynput import keyboard
import pyaudio
import wave
from playsound import playsound
from transcribe import run_whisper

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "file.mp3"

p = pyaudio.PyAudio()

class recorder():
    def __init__(self):
        self.recording = False
        
    def start(self):
        if self.recording: return
        try:
            self.frames = []
            self.stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=self.callback,
                            input_device_index=0)
            print("Stream active:", self.stream.is_active())
            print("start Stream")
            self.recording = True
        except:
            raise

    def stop(self):
        if not self.recording: return
        self.recording = False
        print("Stop recording")
        self.stream.stop_stream()
        self.stream.close()

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
        # playsound(WAVE_OUTPUT_FILENAME)

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.recorder = recorder()
        self.recording = False
        self.shift_r = False

    def flush_input(self):
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            import sys, termios    #for linux/unix
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    def on_press(self, key):
        if not self.recording:
            if type(key) == keyboard._win32.KeyCode:
                if key.char == 'r' or key.char == 'R':
                    print(key.char)
                    self.shift_r = key.char == 'R'
                    self.recorder.start()
                    self.recording = True
                    return True
                if key.char == 'esc':
                    if self.recording:
                        self.recorder.stop()
                        self.recording = False
                    return False
            else:
                if key.name == 'r' or key.name == 'R':
                    self.shift_r = key.name == 'R'
                    self.recorder.start()
                    self.recording = True
                    return True
                if key.name == 'esc':
                    if self.recording:
                        self.recorder.stop()
                        self.recording = False
                    self.flush_input()
                    return False

    def on_release(self, key):
        if type(key) == keyboard._win32.KeyCode:
            if key.char == 'r':
                self.recorder.stop()
                self.recording = False
                if not self.shift_r:
                    self.flush_input()
                    run_whisper()
                    return True
                else:
                    run_whisper()
                    return False
            if key.char == 'R':
                self.recorder.stop()
                self.recording = False
                self.flush_input()
                run_whisper()
                return False
        # Any other key ends the program
        # return False

print("Press and hold the 'r' key to begin recording")
print("Release the 'r' key to end recording")
print("Hold shift and press 'r' to record and exit upon releasing r")
print("Press 'esc' to exit")

# Collect events until released
with MyListener() as listener:
    listener.join()
