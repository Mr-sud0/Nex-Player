import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from PIL import ImageTk,Image

root = Tk()  
 
class MusicPlayer:
    def __init__(self, window ):
        window.geometry('240x400'); window.title('NEXUS Player'); window.resizable(0,0)
        Load = Button(window, text = 'Load',  width = 10, font = ('Times', 10), command = self.load)
        Play = Button(window, text = 'Play',  width = 10,font = ('Times', 10), command = self.play)
        Pause = Button(window,text = 'Pause',  width = 10, font = ('Times', 10), command = self.pause)
        Stop = Button(window ,text = 'Stop',  width = 10, font = ('Times', 10), command = self.stop)
        Load.place(x=80,y=220);Play.place(x=80,y=260);Pause.place(x=80,y=300);Stop.place(x=80,y=340) 
        self.music_file = False
        self.playing_state = False
    def load(self):
        self.music_file = filedialog.askopenfilename()
        song = self.music_file
        song = song.replace(".mp3", "")
        
        tk.Label(text = "Playing:").place(x=0,y=200)
        tk.Label(text = song).place(x=50,y=200)
        self.img = ImageTk.PhotoImage(Image.open("tame.jpg"))
        Label(root, image = self.img).place(x=10,y=10)
            
    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state=True
        else:
            mixer.music.unpause()
            self.playing_state = False
    def stop(self):
        mixer.music.stop()

app= MusicPlayer(root)
root.mainloop()
