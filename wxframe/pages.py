"""

WxFrame pages defined

## Need to add update functions to pages

"""

import tkinter as tk
from tkhtmlview import HTMLLabel
# import nexrad  as nx
# import goes
import buoy
from get_img  import *
from nws_read import get_wrh


class FcstFrame( tk.Frame ):
    def __init__(self, parent, string):
        tk.Frame.__init__(self, parent)#, relief=tk.RAISED)
        
        htmlstyle = '<h6 style="background-color:Black; color:White">'
        
        self.fcst = HTMLLabel(self, html=htmlstyle+string+"</h6>")
        self.fcst.pack()
        
    def disappear(self):
        self.fcst.destroy()
        self.destroy()


class Page00( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = 'Local Forecast'
        # Display image
        self.xx=0.3
        self.yy=0.4
        #self.path = home_meteogram[1]
        
    def show( self ):
        # Home NWS Meteogram
        self.img = Image.open(home_meteogram[1])
        self.homemetimg = ImageTk.PhotoImage(self.img)
        self.homemet = tk.Label(image=self.homemetimg)
        self.homemet.place(anchor='w', relx=0, rely=0.65)
        # Place of interest NWS meteogram
        self.img = Image.open(poi_meteogram[1])
        self.poimetimg = ImageTk.PhotoImage(self.img)
        self.poimet = tk.Label(image=self.poimetimg)
        self.poimet.place(anchor='w', relx=0.5, rely=0.65)
        
        self.fcstframe = FcstFrame( self.parent, get_wrh() )
        self.fcstframe.place(anchor='nw', relx=0, rely=0.06)
        
    def disappear( self ):
        self.homemet.destroy()
        self.poimet.destroy()
        self.fcstframe.disappear()
        
    # def update( self ):
    #     # get images
    #     # self.disappear()
    #     # self.show()
    #     self.after(1800000, self.update)
    #     return


class Page01( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.name = 'Marine'
        # Display image
        self.xx=0.3
        self.yy=0.4
        self.path = cdip_swell[1]
        self.parent = parent
        
    def show( self ):
        self.img = Image.open(self.path)
        self.test = ImageTk.PhotoImage(self.img)
        self.label = tk.Label(image=self.test)
        # Position image
        self.label.place(anchor='center', relx=self.xx, rely=self.yy)
        
        self.parent.tab = buoy.BuoyTable(self.parent)
        self.parent.tab.place(anchor='center', relx=0.75, rely=0.5)
        
    def disappear( self ):
        self.label.destroy()
        self.parent.tab.destroy()


# class Page02( tk.Frame ):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         self.name = 'NEXRAD'
#         self.c    = 0
        
#     def disp( self ):
#         self.img = Image.open(nx.nexrad_loc+nx.nexrad_lst[self.c])
#         self.test = ImageTk.PhotoImage(self.img)
#         self.label = tk.Label(image=self.test)
#         self.label.place(anchor='center', relx=0.5, rely=0.45)
        
#     def show( self ):
#         self.disp()
#         self.cycle()
        
#     def disappear( self ):
#         self.label.destroy()
        
#     def cycle( self ):
#         if self.c == (len(nx.nexrad_lst)-1):
#             self.c = 0
#         else:
#             self.c = self.c + 1
#         self.label.destroy()
#         self.disp()
#         self.label.after(100, self.cycle)
        

# class Page03( tk.Frame ):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         self.parent = parent
#         self.name = 'GOES West Coast'
#         self.c    = 0
        
#     def disp( self ):
#         self.img = Image.open(goes.goes_loc+goes.goes_lst[-self.c])
#         self.test = ImageTk.PhotoImage(self.img)
#         self.label = tk.Label(image=self.test)
#         self.label.place(anchor='center', relx=0.5, rely=0.45)
        
#     def show( self ):
#         self.disp()
#         self.cycle()
        
#     def disappear( self ):
#         self.label.destroy()
        
#     def cycle( self ):
#         if self.c == (len(goes.goes_lst)-1):
#             self.c = 0
#         else:
#             self.c = self.c + 1
#         self.label.destroy()
#         self.disp()
#         self.parent.header.tkraise()
#         self.label.after(100, self.cycle)
        
        
class FullAnimPage( tk.Frame ):
    def __init__(self, parent, page):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = page.name
        self.loc  = page.loc
        self.lst  = page.lst
        self.cdir = page.cdir
        self.c    = 0
    
    def disp( self ):
        self.img = Image.open(self.loc+self.lst[self.cdir*self.c])
        self.test = ImageTk.PhotoImage(self.img)
        self.label = tk.Label(image=self.test)
        self.label.place(anchor='center', relx=0.5, rely=0.45)
        
    def show( self ):
        self.disp()
        self.cycle()
        
    def disappear( self ):
        self.label.destroy()
        
    def cycle( self ):
        if self.name == 'NEXRAD' and self.parent.nexrad_update == True:
            pass
        elif self.name == 'GOES West Coast' and self.parent.goes_update == True:
            pass
        else:
            if self.c == (len(self.lst)-1):
                self.c = 0
            else:
                self.c = self.c + 1
            self.label.destroy()
            self.disp()
            self.parent.header.tkraise()
        self.label.after(100, self.cycle)
    
    
    
    