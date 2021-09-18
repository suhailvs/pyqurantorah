from tkinter import *
from tkinter.ttk import *
from forms.tklistview import MultiListbox
from xml.dom.minidom import parse, parseString

from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

def _init_toolbar(tbmaster):
    tbmaster.tb=Frame(tbmaster.frame,borderwidth=1)
    tbmaster.tb.pack(side=TOP,fill=X)
    tbmaster.btn_view=Button(tbmaster.tb,command=tbmaster.btn_view_click)
    tbmaster.imgedit=PhotoImage(file="static/edit.gif")
    tbmaster.btn_view['image']=tbmaster.imgedit
    tbmaster.btn_view.pack(side=LEFT,padx=4,pady=4)
    

class FormQuran:
    '''The Quran window with toolbar and a datagrid of suras'''
    def __init__(self):
        self.frame=Toplevel()
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_sura=None
        self.suraflag=False # frmasura doesn't exist
        
    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('SL #',3),('Name', 25), ('Type', 25), ('Ayas', 10)))
        suras = parse(path.join(BASE_DIR, 'static/quran-suras.xml'))
        self.update_mlb(items=suras.getElementsByTagName('sura'))
        self.mlb.pack(expand=YES,fill=BOTH)
           
    
    def btn_view_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        if self.suraflag: return 0
        self.suraflag=True
        self.frm_sura=FormSura(self.mlb.item_selected[0])
        self.frame.wait_window(self.frm_sura.frame)
        self.suraflag=False


    def update_mlb(self,items):
        self.mlb.delete(0,END)
        for sura in items:
            index = int(sura.getAttribute('index'))
            total_ayas = sura.getAttribute('ayas')
            # name = s.getAttribute('name')
            tname = sura.getAttribute('tname')
            mecca_medina = sura.getAttribute('type')
            self.mlb.insert(END, (index,tname,mecca_medina, total_ayas))

        self.mlb.selection_set(0) #set first row selected

           
class FormSura:
    '''View selected sura with all ayas in arabic'''
    def __init__(self,sura=1):
        self.sura = sura
        self.frame=Toplevel()
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()
        
    def _init_widgets(self):
        all_ayas = parse(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'static/quran-ayas.xml'))
        sura_ayas = all_ayas.getElementsByTagName('sura')[self.sura - 1].getElementsByTagName('aya')
        texts = ''
        for aya_text in sura_ayas:
            texts+=aya_text.getAttribute('text')

        self.label1=Label(self.frame,text=texts)
        self.label1.grid(row=0,sticky=W)
        
    def callback(self):
        print ('user exits the screen')
        self.frame.destroy()
           