# from tkinter import *
# from tkinter.ttk import *

import tkinter as tk
from forms.tklistview import MultiListbox
from forms.tkcalendar import ttkCalendar
from xml.dom.minidom import parse, parseString

from os import path


        
from awesometkinter.bidirender import add_bidi_support     # https://github.com/Aboghazala/AwesomeTkinter
import arabic_reshaper                                     # https://github.com/mpcabd/python-arabic-reshaper


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

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
        suras = parse(path.join(BASE_DIR, 'static/quran-suras.xml'))
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
        all_ayas = parse(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'static/quran-ayas.xml'))
        sura_ayas = all_ayas.getElementsByTagName('sura')[self.sura].getElementsByTagName('aya')

        return [aya_text.getAttribute('text') for aya_text in sura_ayas]

    def lbl_click(self,event,n=0):
        print(event,n)

    def _init_widgets(self):
        lbls = []
        for n,aya_text in enumerate(self.get_ayas()):
            lbl = tk.Label(self.frame, anchor="e", width=35, font=("Helvetica", 22), bg='white',pady=5, relief = 'ridge') #, border="ridge" )
            lbl.grid(column = 0, row = n)
            lbl.bind( "<Button>", lambda event, lbl_n=n: self.lbl_click(event, lbl_n) )

            ctxt=arabic_reshaper.reshape(aya_text)
            add_bidi_support(lbl)
            lbl.set(f'({n+1}) {ctxt}') # 'السلام عليكم')
            # lbls.append(lbl)


    
    def aya_click(self, event):
        print(event.num)

    def callback(self):
        print ('user exits the screen')
        self.frame.destroy()
           