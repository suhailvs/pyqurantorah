# from tkinter import *
# from tkinter.ttk import *

import tkinter as tk
from forms.tklistview import MultiListbox
from forms.tkcalendar import ttkCalendar
from xml.dom.minidom import parse, parseString

import os, time
from os import path


        
from awesometkinter.bidirender import add_bidi_support     # https://github.com/Aboghazala/AwesomeTkinter
import arabic_reshaper                                     # https://github.com/mpcabd/python-arabic-reshaper
import vlc                                                 # pip install python-vlc (https://github.com/oaubert/python-vlc)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _init_toolbar(tbmaster):
    tbmaster.tb=tk.Frame(tbmaster.frame,borderwidth=1)
    tbmaster.tb.pack(side=tk.TOP,fill=tk.X)

    tbmaster.btn_view=tk.Button(tbmaster.tb,command=tbmaster.btn_view_click)
    tbmaster.img_view=tk.PhotoImage(file="static/edit.gif")
    tbmaster.btn_view['image']=tbmaster.img_view
    tbmaster.btn_view.pack(side=tk.LEFT,padx=4,pady=4)
    
    tbmaster.btn_view2=tk.Button(tbmaster.tb,command=tbmaster.btn_view2_click)
    tbmaster.img_view2=tk.PhotoImage(file="static/edit2.gif")
    tbmaster.btn_view2['image']=tbmaster.img_view2
    tbmaster.btn_view2.pack(side=tk.LEFT,padx=4,pady=4)



class FormQuran:
    '''The Quran window with toolbar and a datagrid of suras'''
    def __init__(self):
        self.frame=tk.Toplevel()
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_sura=None
        self.frm_sura2=None
        self.suraflag=False # frmasura doesn't exist
        
    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('SL #',3),('Name', 25), ('Type', 25), ('Ayas', 10)))
        suras = parse(os.path.join(BASE_DIR, 'static/quran-suras.xml'))
        self.update_mlb(items=suras.getElementsByTagName('sura'))
        self.mlb.pack(expand=tk.YES,fill=tk.BOTH)
           
    
    def btn_view_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        if self.suraflag: return 0
        self.suraflag=True
        self.frm_sura=FormSura(self.mlb.item_selected[0])
        self.frame.wait_window(self.frm_sura.frame)
        self.suraflag=False

    def btn_view2_click(self):
        if self.frm_sura2==None:
            self.frm_sura2=ttkCalendar(master=self.frame)
        elif self.frm_sura2.flag:
            return 0
        else:
            self.frm_sura2=ttkCalendar(master=self.frame)
            
        self.frame.wait_window(self.frm_sura2.top)
        print (self.frm_sura2.datepicked)

    def update_mlb(self,items):
        self.mlb.delete(0,tk.END)
        for sura in items:
            index = int(sura.getAttribute('index'))
            total_ayas = sura.getAttribute('ayas')
            # name = s.getAttribute('name')
            tname = sura.getAttribute('tname')
            mecca_medina = sura.getAttribute('type')
            self.mlb.insert(tk.END, (index,tname,mecca_medina, total_ayas))

        self.mlb.selection_set(0) #set first row selected

           
class FormSura:
    '''View selected sura with all ayas in arabic'''
    def __init__(self,sura=1):
        self.sura = sura
        self.frame=tk.Toplevel()
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
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
            for i in range(10):
                if os.path.exists(f'{fname}{i+1}.bin'):
                    self.play_audio(f'{fname}{i+1}.bin')
                else:
                    break
        else:
            print('file doesnt exists')
        lbl['fg']='black'

    def _init_widgets(self):
        for n,aya_text in enumerate(self.get_ayas()):
            lbl = tk.Label(self.frame, anchor="e", width=35, font=("Helvetica", 22), bg='white',pady=5, relief = 'ridge') #, border="ridge" )
            lbl.grid(column = 0, row = n)
            ctxt=arabic_reshaper.reshape(aya_text)
            add_bidi_support(lbl)
            lbl.set(f'({n+1}) {ctxt}')
            lbl.bind( "<Button>", lambda event, lbl_n=n, lbl=lbl: self.lbl_click(event, lbl_n, lbl))
    

    def callback(self):
        print ('user exits the screen')
        self.frame.destroy()
           