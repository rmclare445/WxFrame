"""

WxFrame pages defined

"""

import tkinter as tk
import nexrad  as nx
from get_img  import *


class Page00( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.name = 'Local Forecast'
        # Display image
        self.xx=0.3
        self.yy=0.4
        self.path = nws_meteogram[1]
        
    def show( self ):
        self.img = Image.open(self.path)
        self.test = ImageTk.PhotoImage(self.img)
        self.label = tk.Label(image=self.test)
        self.label.image = self.test
        # Position image
        self.label.place(anchor='center', relx=self.xx, rely=self.yy)
        
    def disappear( self ):
        self.label.destroy()


class Page01( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.name = 'Marine'
        # Display image
        self.xx=0.3
        self.yy=0.4
        self.path = cdip_swell[1]
        
    def show( self ):
        self.img = Image.open(self.path)
        self.test = ImageTk.PhotoImage(self.img)
        self.label = tk.Label(image=self.test)
        self.label.image = self.test
        # Position image
        self.label.place(anchor='center', relx=self.xx, rely=self.yy)
        
    def disappear( self ):
        self.label.destroy()


class Page02( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.name = 'NEXRAD'
        self.c    = 0
        
    def disp( self ):
        self.img = Image.open(nx.nexrad_loc+nx.nexrad_lst[self.c])
        self.test = ImageTk.PhotoImage(self.img)
        self.label = tk.Label(image=self.test)
        self.label.image = self.test
        self.label.place(anchor='center', relx=0.5, rely=0.45)
        
    def show( self ):
        self.disp()
        self.cycle()
        
    def disappear( self ):
        self.label.destroy()
        
    def cycle( self ):
        if self.c == 19:
            self.c = 0
        else:
            self.c = self.c + 1
        self.label.destroy()
        self.disp()
        self.label.after(100, self.cycle)