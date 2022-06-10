import tkinter as tk
import threading
import requests
import json
import subprocess

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.lastWord = ""

        self.label = tk.Label(self, text="Word : ")
        self.label.grid(row=0, column=0)
        self.wordEnt = tk.Entry(self, width="50")
        self.wordEnt.focus()
        self.wordEnt.bind("<Control-BackSpace>", self.controlBackspacePressed)
        self.wordEnt.bind("<KeyRelease>", self.wordEntKeyRelease)
        self.wordEnt.bind("<Down>", self.keyDownPressed)
        self.wordEnt.bind("<Return>", self.keyEnterPressed)
        self.wordEnt.grid(row=0, column=1)

        self.wordList = tk.Listbox(self, width="50")
        self.wordList.bind("<Down>", self.wordListKeyPressed)
        self.wordList.bind("<Up>", self.wordListKeyPressed)
        self.wordList.bind("<Return>", self.wordListEnterKeyPressed)
        
        # Get env file info
        try:
            envFile = open("/home/.config/simple-google-translator-python/env.txt", "r")
            envFileContent = envFile.read().split("\n")
            envFile.close()
            envFileContentDict = {}
            for info in envFileContent:
                info = info.split("=")
                envFileContentDict[info[0]] = info[1]
            envFileContent = envFileContentDict
            self.srcLang = envFileContent['SourceLanguage'] #source language
            self.desLang = envFileContent['DestinationLanguage'] #destination language
        except:
            self.srcLang = "auto" #source language
            self.desLang = "fa" #destination language
            
    def controlBackspacePressed(self, event):
        entryValue = self.wordEnt.get()
        if(entryValue == ""):
            return
        entryValue = entryValue.split(" ")
        entryValue.pop()
        entryValue = " ".join(entryValue) + " "
        self.wordEnt.delete(0, tk.END)
        self.wordEnt.insert(0, entryValue)

    def keyDownPressed(self, event):
        self.lastWord = self.wordEnt.get()
        if(self.wordList.size() != 0):
            self.wordList.focus()
            self.wordList.select_set(0)
            self.lastWord = self.wordEnt.get()
            self.wordEnt.delete(0, tk.END)
            self.wordEnt.insert(0, self.wordList.get(0))
    def keyEnterPressed(self, event):
        word = self.wordEnt.get()
        if(word != ""):
            self.translate(word)
        
    def wordEntKeyRelease(self, event):
        if (event.state == 20 and event.keysym == "BackSpace"):
            return
        if (event.keysym == "Down"):
            return
        word = self.wordEnt.get()
        if(word.strip() == ""):
            self.wordList.grid_forget()
            return
        else:
            autoCompleteThread = threading.Thread(target=self.auto_complete_req, args=(word, ))
            autoCompleteThread.start()

    def wordListKeyPressed(self, event):
        if (event.keysym == "Up"):
            if(self.wordList.curselection()[0] == 0):
                self.wordEnt.delete(0, tk.END)
                self.wordEnt.insert(0, self.lastWord)
                self.wordEnt.focus()
                return

        for i in self.wordList.curselection():
            if(event.keysym == "Up"):
                w = self.wordList.get(self.wordList.curselection()[0] - 1)
            elif event.keysym == "Down":
                if(i == self.wordList.size() - 1):
                    return
                w = self.wordList.get(self.wordList.curselection()[0] + 1)
            self.wordEnt.delete(0, tk.END)
            self.wordEnt.insert(0, w)

    def wordListEnterKeyPressed(self, event):
        if(len(self.wordList.curselection()) != 0):
            word = self.wordList.get(self.wordList.curselection()[0])
            self.wordEnt.delete(0, tk.END)
            self.wordEnt.insert(0, word)
            self.wordEnt.focus()
            self.translate(self.wordEnt.get())

    def auto_complete_req(self, q):
        req = requests.get("https://abadis.ir/ajaxcmd/getaclist/?exp=" + q)
        content = req.text[1:].split("</span>")
        content.pop()

        for word in content:
            index = content.index(word)
            word = word.replace("<i class='ico icoSr'></i>", "")
            word = word.replace("<span>", "")
            content[index] = word
        if (content == []):
            self.wordList.grid_forget()
            return
        self.wordList.config(listvariable=tk.StringVar(value=content))
        self.wordList.grid(row=1, column=1)

    def translate(self, word):
        req = requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + self.srcLang + "&tl=" + self.desLang + "&hl=en-US&dt=t&dt=bd&dj=1&source=input&tk=29979.29979&q=" + word)

        t = json.loads(req.text)
        trans = t['sentences'][0]['trans']
        try :
            terms = t['dict'][0]['terms']
            for i in terms:
                trans += ", " + i
        except:
            pass

        subprocess.Popen(['notify-send', trans])
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Google Translator")
    App(root).grid(padx="5", pady="5")
    root.mainloop()