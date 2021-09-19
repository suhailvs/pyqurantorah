import tkinter as tk
import os, time
from xml.dom.minidom import parse

from awesometkinter.bidirender import add_bidi_support     # https://github.com/Aboghazala/AwesomeTkinter
import arabic_reshaper                                     # https://github.com/mpcabd/python-arabic-reshaper
import vlc                                                 # pip install python-vlc (https://github.com/oaubert/python-vlc)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FormSuraScrollable(tk.Frame):
    def __init__(self, sura):
        self.parent=tk.Toplevel()
        self.parent.wm_geometry("630x700") # width x height
        tk.Frame.__init__(self, self.parent)
        self.sura = sura
        
        self.parent.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        
        self.canvas = tk.Canvas(self, borderwidth=0, background="white")
        self.frame = tk.Frame(self.canvas, background="white")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw",tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self._init_widgets()

    def get_ayas(self):
        all_ayas = parse(os.path.join(BASE_DIR, 'static/quran-ayas.xml'))
        sura_ayas = all_ayas.getElementsByTagName('sura')[self.sura].getElementsByTagName('aya')

        return [aya_text.getAttribute('text') for aya_text in sura_ayas]
    def play_audio(self,fname):
        print(f'going to play {fname}')
        p=vlc.MediaPlayer(fname)
        p.play()
        time.sleep(0.5)  # sleep because it needs time to start playing
        while p.is_playing():
            time.sleep(0.5)  # sleep to use less CPU

    def lbl_click(self,event,n,lbl):
        if event.num != 1:
            # if not left button clicked
            return

        lbl['fg']='red'
        self.frame.update()

        fname = os.path.join(BASE_DIR,'static','audio',f'S{self.sura+1}_{n+1}_') # f'S98_1_0.bin'
        if os.path.exists(f'{fname}0.bin'):
            print('only 1 file')
            self.play_audio(f'{fname}0.bin')
        elif os.path.exists(f'{fname}1.bin'):
            print('more than 1 file')
            # eg 5-2,6-2,8-3
            for i in range(20):
                if os.path.exists(f'{fname}{i+1}.bin'):
                    self.play_audio(f'{fname}{i+1}.bin')
                else:
                    break
        else:
            print('file doesnt exists')
        lbl['fg']='black'

    def _init_widgets(self):
        for n,aya_text in enumerate(self.get_ayas()):
            # https://github.com/googlefonts/noto-fonts/tree/main/hinted/ttf/NotoSansArabic
            lbl = tk.Label(self.frame, anchor="e", width=35, font=("Noto Sans Arabic", 22), bg='white',pady=5, relief = 'ridge') # bold, lighter,
            lbl.grid(column = 0, row = n)
            ctxt=arabic_reshaper.reshape(aya_text)
            wrapped_text = ''
            for i in range(0,len(ctxt),40): wrapped_text+=f'{ctxt[i:i+40]}\n' # letter wrap

            add_bidi_support(lbl)
            lbl.set(f'({n+1}) {wrapped_text}')
            lbl.bind( "<Button>", lambda event, lbl_n=n, lbl=lbl: self.lbl_click(event, lbl_n, lbl))


    def callback(self):
        print ('user exits the screen')
        self.parent.destroy()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
