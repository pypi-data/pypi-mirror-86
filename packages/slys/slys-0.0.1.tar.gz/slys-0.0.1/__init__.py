# Modules

import os, playsound, webbrowser as web

class Using:
    def openFile(self, file):
        os.startfile(file)

    def StartSound(self, soundfile):
        playsound.playsound(soundfile)

    def open_url(self, url):
        web.open(url)
