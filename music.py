import io
import os
import PIL.Image
import stagger
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from PIL import ImageTk
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk


root = ThemedTk(theme="arc")
root.config(bg='#F0FFFF')

def set_vol(val):
    volume = float(val) / 100
    mixer.init()
    mixer.music.set_volume(volume)
    
class MusicPlayer:
    def __init__(self, window ):
        window.geometry('240x400'); window.title('NEXUS Player'); window.resizable(300,600)
        Load = ttk.Button(window, text = 'Load',  width = 10, command = self.load)
        Play = ttk.Button(window, text = 'Play',  width = 10, command = self.play)
        Pause = ttk.Button(window,text = 'Pause',  width = 10, command = self.pause)
        Stop = ttk.Button(window ,text = 'Stop',  width = 10, command = self.stop)
        volume = PIL.Image.open("speaker.png")
        volume = volume.resize((20, 20))
        self.vol = ImageTk.PhotoImage(volume)
        p_vol= ttk.Label(root, image = self.vol).place(x=20,y=365)
        Load.place(x=80,y=220);Play.place(x=80,y=260);Pause.place(x=80,y=300);Stop.place(x=80,y=340) 
        self.music_file = False
        self.playing_state = False

    def load(self):
        imageFile = PIL.Image.open("player.png")
        imageFile = imageFile.resize((215, 170))
        self.photo = ImageTk.PhotoImage(imageFile)
        p_img=ttk.Label(root, image = self.photo).place(x=10,y=10)

        name=tk.Label(text = "                                                                                                                ").place(x=50,y=200)
        self.music_file = filedialog.askopenfilename(parent=root, title='Choose an audio File', filetypes=[(".mp3, .flac, .wav, .ogg", "*.mp3; *.flac;*.wav;*.ogg")])
        song = self.music_file
        mp3 = stagger.read_tag(self.music_file)
        by_data = mp3[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)
        imageFile = PIL.Image.open(im)
        imageFile = imageFile.resize((215, 170))
        self.photo = ImageTk.PhotoImage(imageFile)
        
        song = os.path.basename(self.music_file)
        song = song.replace(".mp3", "")
        
        ttk.Label(text = "Playing:").place(x=0,y=200)
        name=ttk.Label(text = song).place(x=50,y=200)
 
        p_img=ttk.Label(root, image = self.photo).place(x=10,y=10)
            
    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            pass
    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state=True
        else:
            mixer.music.unpause()
            self.playing_state = False

    def stop(self):
        mixer.music.stop()


ttk.Progressbar(root,length=220,orient='horizontal',value=40,mode='determinate').pack(pady=185)
scale = ttk.Scale(root, from_=100, to=0,length=140,orient=VERTICAL, command=set_vol)
scale.place(x=20,y=225)
scale.set(50)  # implement the default value of scale when music player starts
mixer.init()
mixer.music.set_volume(0.5)
app= MusicPlayer(root)
root.mainloop()
