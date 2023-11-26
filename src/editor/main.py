import tkinter as tk
import librosa
import pygame
import time

AUDIO_FILE = "./data/sample.wav"


def beat_detect(audio_file):
    y, sr = librosa.load(audio_file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr) # convert beat frames to time
    return beat_times


def display_beats():
    beat_times = beat_detect(AUDIO_FILE)

    # play audio
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

    # display beat hits
    beat_index = 0
    while pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000.0  # convert to seconds
        if beat_index < len(beat_times) and current_time >= beat_times[beat_index]:
            existing_text = label.cget("text")
            label.config(text=existing_text + ' •')
            root.update()
            beat_index += 1
        else:
            time.sleep(0.01)


# GUI
root = tk.Tk()
btn = tk.Button(root, text='Detect Beats', command=display_beats)
btn.pack()
label = tk.Label(root, text='')
label.pack()
root.mainloop()
