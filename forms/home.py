# from tkinter import *
# from tkinter.ttk import *
from forms.quran import FormQuran


import tkinter as tk
class FormMenu:
    """This is the main form that shows after user login.
    Contains
    =========
    --> Three Buttons
        --> Quran:   OnClick Shows FormQuran,
        --> Torah:   OnClick Shows FormTorah,
    --> A background Image
    """
    def __init__(self,master):
        self.frame=master
        # self._init_menu()
        self._init_widgets()
        
    def _init_widgets(self):
        # style = tk.Style()
        # style.configure("BW.TLabel", foreground="white", background="black")
        self.buttons = tk.Frame(self.frame)
        self.btnquran = tk.Button(self.buttons,command=self.quran_click)
        self.imgprdt=tk.PhotoImage(file="static/invoices.gif")
        self.btnquran['image']=self.imgprdt
        self.btnquran.pack(side='top')
        lbl1=tk.Label(self.buttons,text="Quran...").pack()
        self.buttons.pack(side='left',padx=10)

        #background label
        #-------------------------------------------
        self.imgback=tk.PhotoImage(file="static/back.gif")
        self.lblbackground= tk.Label(self.frame,borderwidth=0)
        self.lblbackground.pack(side='top')
        self.lblbackground['image'] = self.imgback

    
    


    def quran_click(self):
        self.frame.withdraw()
        self.frm_products=FormQuran()
        self.frame.wait_window(self.frm_products.frame)
        self.frame.deiconify()
        