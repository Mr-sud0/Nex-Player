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
from tkinter import ttk                         # Normal Tkinter.* widgets are not themed!
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tinytag import TinyTag
import time 


root = ThemedTk(theme="adapta")
root.config(bg='#F0FFFF')
photo = PhotoImage(file = 'icon.png')
root.iconphoto(False, photo)

##################......VARIABLES......#######################
song_len = 0
v_store = DoubleVar()
val = DoubleVar()


##################......MUSIC PROGRESSBAR......########################
p1 = ttk.Progressbar(root, length=210, cursor='spider',
                     mode="determinate",
                     orient=tk.HORIZONTAL)
p1.pack(pady=220)



#################.......VOLUME METHOD TO SET VOLUME........#############
def set_vol(val):
    volume = float(val) / 100
    mixer.init()
    mixer.music.set_volume(volume)


###################.....CLASS.....#######################
class MusicPlayer:

#################.....METHOD TO INITIALIZE THE OBJECTS ON WINDOW......###########

    def __init__(self, window ):
        
        window.geometry('230x460'); window.title('NEXUS'); window.resizable(0,0)

        s_load = PIL.Image.open("load.png")
        s_load = s_load.resize((208, 208))
        self.m_load = ImageTk.PhotoImage(s_load)
        ttk.Label(root, image = self.m_load).place(x=10,y=5)
        ttk.Label(text = "Select an audio file.",borderwidth=0).place(x=65,y=230)


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
        tk.Button(window, image = self.vol, borderwidth=0, command=self.muted).place(x=20,y=410)

        Load.place(x=90,y=255);Play.place(x=90,y=300);Pause.place(x=90,y=345);Stop.place(x=90,y=390) 

        self.music_file = False

        self.playing_state = False

############.....LOAD BUTTON METHOD.....##############
    def load(self):
        
        tk.Label(text = "                                                                                                                ").place(x=50,y=230)
        self.music_file = filedialog.askopenfilename(parent=root, title='Choose an audio File', filetypes=[(".mp3, .flac, .wav, .ogg", "*.mp3; *.flac;*.wav;*.ogg")])
        s_len = TinyTag.get(self.music_file)
        song = self.music_file
        song = os.path.basename(self.music_file)

        imageFile = PIL.Image.open("player.png")
        imageFile = imageFile.resize((208, 208))
        self.photo = ImageTk.PhotoImage(imageFile)
        p_img=ttk.Label(root, image = self.photo).place(x=10,y=5)

        song = song.replace(".mp3", "")
        ttk.Label(text = "Playing:").place(x=0,y=230)
        name=ttk.Label(text = song).place(x=50,y=230)
        global song_len
        
        song_len = int(s_len.duration)
        
        
        mp3 = stagger.read_tag(self.music_file)
        
        by_data = mp3[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)
        imageFile = PIL.Image.open(im)
        imageFile = imageFile.resize((208, 208))
        self.photo = ImageTk.PhotoImage(imageFile)
        
        p_img=ttk.Label(root, image = self.photo).place(x=10,y=5)
           
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

############.....MUTE BUTTON METHOD.....##############


    def muted(self):
        global v_store
        v_store= int(val.get())
        scale.set(0)
        self.mute = PIL.Image.open("mute.png")
        self.mute = self.mute.resize((20, 20))
        self.mute = ImageTk.PhotoImage(self.mute)
        tk.Button(root, image = self.mute, borderwidth=0, command= self.unmute).place(x=20,y=410)


############.....UNMUTE BUTTON METHOD.....##############

    def unmute(self):
        scale.set(v_store)
        volume = PIL.Image.open("speaker.png")
        volume = volume.resize((20, 20))
        self.vol = ImageTk.PhotoImage(volume)
        tk.Button(root, image = self.vol, borderwidth=0, command=self.muted).place(x=20,y=410)


############.....MUSIC PROGRESSBAR METHOD.....##############

def progress():
    mixer.init()
    p1['maximum']= song_len
    p1["value"] = mixer.music.get_pos()// 1000
    
    p1.after(2,progress)
    

progress()       #....METHOD CALLS ITSELF


############.....VOLUME SCALE.....##############

scale = ttk.Scale(root,variable= val, from_=100, to=0,length=150,orient=VERTICAL, command=set_vol)

scale.place(x=20,y=260)

scale.set(50)        #... implement the default value of scale when music player starts
mixer.init()    #... MIXER INITIALIZING

mixer.music.set_volume(0.5)     #... SET DEAFULT VOLUME


app= MusicPlayer(root)
root.mainloop()
