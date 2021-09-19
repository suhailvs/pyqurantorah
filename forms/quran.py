import tkinter as tk
from forms.tklistview import MultiListbox
from forms.tkcalendar import ttkCalendar
from forms.sura import FormSuraScrollable
from xml.dom.minidom import parse

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _init_toolbar(tbmaster):
    tbmaster.tb=tk.Frame(tbmaster.frame,borderwidth=1)
    tbmaster.tb.pack(side=tk.TOP,fill=tk.X)

    tbmaster.btn_view=tk.Button(tbmaster.tb,command=tbmaster.btn_view_click)
    tbmaster.img_view=tk.PhotoImage(file="static/edit.gif")
    tbmaster.btn_view['image']=tbmaster.img_view
    tbmaster.btn_view.pack(side=tk.LEFT,padx=4,pady=4)
    
    # not used just for test
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
        self.frm_sura=FormSuraScrollable(self.mlb.item_selected[0])
        self.frm_sura.pack(side="top", fill="both", expand=True)
        self.frame.wait_window(self.frm_sura.frame)
        self.suraflag=False

    def btn_view2_click(self):
        # not used just for test
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

           