##################......DEPENDENCIES MODULES......##################
import io
import os
import PIL.Image
import stagger
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import mutagen
from mutagen.mp3 import MP3
from PIL import ImageTk
from tkinter import ttk                    # Normal Tkinter.* widgets are not themed!
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tinytag import TinyTag
import time 

##############.......CREATING ROOT WINDOW.......###############

root = ThemedTk(theme="adapta")
root.config(bg='#F0FFFF')
photo = PhotoImage(file = 'icon.png')
root.iconphoto(False, photo)

##################......VARIABLES......#######################

song_len = 0



##################......MUSIC PROGRESSBAR......########################

p1 = ttk.Progressbar(root, length=215, cursor='spider',
                     mode="determinate",
                     orient=tk.HORIZONTAL)
p1.pack(pady=190)



#################.......VOLUME METHOD TO SET VOLUME........#############

def set_vol(val):
    volume = float(val) / 100
    mixer.init()
    mixer.music.set_volume(volume)



###################.....CLASS.....#######################

class MusicPlayer:

#################.....METHOD TO INITIALIZE THE OBJECTS ON WINDOW......###########

    def __init__(self, window ):
        window.geometry('240x400'); window.title('NEXUS Player'); window.resizable(0,0)

        loadimg = PIL.Image.open("folder.png")
        loadimg = loadimg.resize((35, 35))
        self.load_p = ImageTk.PhotoImage(loadimg)
        Load = Button(window, image=self.load_p,width = 0, command = self.load)

        playimg = PIL.Image.open("play.png")
        playimg = playimg.resize((35, 35))
        self.play_p = ImageTk.PhotoImage(playimg)
        Play = Button(window, image=self.play_p, width = 0, command = self.play)

        pauseimg = PIL.Image.open("pause.png")
        pauseimg = pauseimg.resize((35, 35))
        self.pause_p = ImageTk.PhotoImage(pauseimg)
        Pause = Button(window, image=self.pause_p, width = 0, command = self.pause)

        stopimg = PIL.Image.open("stop.png")
        stopimg = stopimg.resize((35, 35))
        self.stop_p = ImageTk.PhotoImage(stopimg)
        Stop = Button(window, image=self.stop_p, width = 0, command = self.stop)

        volume = PIL.Image.open("speaker.png")
        volume = volume.resize((20, 20))
        self.vol = ImageTk.PhotoImage(volume)
        p_vol= ttk.Label(root, image = self.vol).place(x=20,y=365)

        Load.place(x=100,y=215);Play.place(x=100,y=260);Pause.place(x=100,y=305);Stop.place(x=100,y=350) 

        self.music_file = False

        self.playing_state = False

############.....LOAD BUTTON METHOD.....##############

    def load(self):
        imageFile = PIL.Image.open("player.png")
        imageFile = imageFile.resize((215, 170))
        self.photo = ImageTk.PhotoImage(imageFile)
        p_img=ttk.Label(root, image = self.photo).place(x=10,y=10)

        name=tk.Label(text = "                                                                                                                ").place(x=50,y=200)
        
        self.music_file = filedialog.askopenfilename(parent=root, title='Choose an audio File', filetypes=[(".mp3, .flac, .wav, .ogg", "*.mp3; *.flac;*.wav;*.ogg")])
        s_len = TinyTag.get(self.music_file)
        song = self.music_file
        song = os.path.basename(self.music_file)
        song = song.replace(".mp3", "")
        ttk.Label(text = "Playing:").place(x=0,y=200)
        name=ttk.Label(text = song).place(x=50,y=200)
        
        global song_len
        song_len = int(s_len.duration)

        
        
        mp3 = stagger.read_tag(self.music_file)
        
        by_data = mp3[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)
        imageFile = PIL.Image.open(im)
        imageFile = imageFile.resize((215, 170))
        self.photo = ImageTk.PhotoImage(imageFile)
        p_img = ttk.Label(root, image = self.photo).place(x=10,y=10)
           
############.....PLAY BUTTON METHOD.....##############

    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            pass

############.....PAUSE BUTTON METHOD.....##############

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state=True
        else:
            mixer.music.unpause()
            self.playing_state = False

############.....STOP BUTTON METHOD.....##############

    def stop(self):
        mixer.music.stop()

############.....MUSIC PROGRESSBAR METHOD.....##############

def progress():
    mixer.init()
    p1['maximum']= song_len
    p1["value"] = mixer.music.get_pos()// 1000
    
    p1.after(2,progress)

progress()       #....METHOD CALLS ITSELF

############.....VOLUME SCALE.....##############

scale = ttk.Scale(root, from_=100, to=0,length=140,orient=VERTICAL, command=set_vol)

scale.place(x=20,y=225)

scale.set(50)        #... implement the default value of scale when music player starts

mixer.init()    #...MIXER INITIALIZING

mixer.music.set_volume(0.5)     #...SET DEAFULT VOLUME


app= MusicPlayer(root)
root.mainloop()
