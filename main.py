#!/usr/bin/python3 

import tkinter
from tkinter import ttk
import requests
import json
import subprocess
import threading

def one_less_word(ev):
    value = ent.get().split(" ")
    value = value[0:-1]
    value = " ".join(value)
    ent.delete(0, tkinter.END)
    ent.insert(0, value)

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



def auto_complete_req(q):
    req = requests.get("https://api.datamuse.com/words?sp=" + q + "*")
    values = json.loads(req.text)
    values_list = []
    for v in values:
        values_list.append(v['word'])
    print(values_list)


def callback(sv):
    q = sv.get()
    if(q != ""):
        threading.Thread(target=auto_complete_req, args=(q, )).start()
    
root = tkinter.Tk()
root.title("Google Translator")

frame = ttk.Frame(root, padding="12 12 12 12")
frame.pack(fill="x")

sv = tkinter.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))


entFrame = ttk.Frame(frame, padding="0 0 0 0")
ent = tkinter.Entry(entFrame, width="50", textvariable=sv)
ent.focus()
ent.grid()
entFrame.pack(fill="x")

root. bind('<Return>', translate)
root. bind('<Control-BackSpace>', one_less_word)

root.mainloop()