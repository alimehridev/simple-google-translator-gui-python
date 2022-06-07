#!/usr/bin/python3 

import tkinter
from tkinter import ttk
import requests
import json
import subprocess

def createEntry(value = ""):
    entFrame = ttk.Frame(frame, padding="0 0 0 7")
    global lbl
    lbl = ttk.Label(entFrame, text="Word: ")
    lbl.grid()
    global ent
    ent = tkinter.Entry(entFrame, width="50")
    ent.focus()
    ent.insert(0, value)
    ent.grid()
    entFrame.pack(fill="x")

# def createBtn():
#     btn = tkinter.Button(frame, text="Translate", command=translate)
#     btn.pack(fill="x")

def translate(ev):
    word = ent.get()
    if word == "":
        return
    
    req = requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=fa&hl=en-US&dt=t&dt=bd&dj=1&source=input&tk=29979.29979&q=" + word)

    t = json.loads(req.text)
    trans = t['sentences'][0]['trans']
    try :
        terms = t['dict'][0]['terms']
        for i in terms:
            trans += ", " + i
    except:
        pass

    subprocess.Popen(['notify-send', trans])
    root.destroy()

root = tkinter.Tk()
root.title("Google Translator")
frame = ttk.Frame(root, padding="12 12 12 12")
frame.pack(fill="x")


createEntry()
root. bind('<Return>', translate)

root.mainloop()