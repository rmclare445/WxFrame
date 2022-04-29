"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

## should add tides to dashboard

## buoy table on Pacific page

## integrate with thermostat and ESP-2866 weather station

## update cycles every minute but with specific time conditionals

"""

import tkinter as tk
#from tkinter  import ttk
import nexrad as nx
from get_img  import *
from riseset  import get_riseset
from nws_read import get_synopsis
from time     import strftime


class WxFrame( tk.Tk ):
    def __init__( self ):
        super().__init__()
        
        # Configure attributes
        self.title("WxFrame")
        self.configure(bg='black', cursor="none")
        self.attributes('-fullscreen', True)
        self.globfont = 'lucida'
        # Clarify initialization period
        self.init = True
        self.current_page = 0
        # Exit on Esc
        self.bind( "<Escape>", lambda x: self.destroy() )
        # Turn page on Enter ## will be amended to GPIO input on Pi
        #self.bind( "<Return>", lambda x: self.turn_page() )
        # Bind all the number keys with the callback function
        for i in range(10):
           self.bind(str(i), self.toggle_page)
        
        # Get screen resources
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Get new images
        print("Getting updated images")
        #get_imgs()
        #nx.get_nexrad()
        print("Updated images retrieved")
        
        # Establish pages
        self.pages = ['Local', 'CONUS', 'Pacific', 'Global', 'Forecast']
        
        # Make header with page name
        self.header = tk.Frame( self, relief=tk.RAISED, borderwidth=4 )
        self.header.place(relx=0, rely=0, anchor="nw")
        self.headtext = tk.Label( self.header, text="Local" )
        self.headtext.pack( )
        self.headtext.config(fg="white", bg="black", 
                             font=(self.globfont, int(self.height/36.), 'italic'),
                             padx=10, pady=5)
        
        # Display dashboard
        self.dash = Dashboard(self)
        # Display first page
        self.p00 = Page00(self)
        self.p01 = Page01(self)
        self.p02 = Page02(self)
        self.ps  = [self.p00, self.p01, self.p02]
        self.ps[0].show()
        
        # Initialization period over
        self.init = False
        
    def turn_page( self ):
        #
        self.ps[self.current_page].disappear()
        if self.current_page < 2:
            self.current_page+=1
        else:
            self.current_page = 0
        # self.headtext.config(text = self.pages[self.current_page])
        # self.dash.update_synopsis( self )
        #self.current_page = abs( self.current_page - 1 )
        self.ps[self.current_page].show()
        
    def toggle_page( self, n ):
        #
        self.ps[self.current_page].disappear()
        self.current_page = int(n.char)
        self.ps[self.current_page].show()


class Page00( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
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
        self.c =0
        
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


class Dashboard( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, borderwidth=4 )
        self.place(relx=0, rely=1, anchor="sw")
        self.dash_font = (parent.globfont, int(parent.height/40.), 'bold')
        
        # Make clock
        self.clock = tk.Label(self, text="")
        self.clock.pack(side=tk.LEFT, fill=tk.BOTH)
        self.clock.config(fg="white", bg="navy", font=self.dash_font,
                          padx=20, pady=15)
        self.update_clock( )
        # Make sunrise/set label
        self.riseset = tk.Label(self, text="")
        self.riseset.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.riseset.config(fg="white", bg="red", font=self.dash_font,
                            padx=10, pady=15)
        self.update_riseset( parent )
        # Make exterior data label
        self.exterior = tk.Label(self, text="52\u00B0\n31\u00B0")
        self.exterior.pack(side=tk.LEFT, fill=tk.BOTH)
        self.exterior.config(fg="white", bg="grey2", font=self.dash_font,
                            padx=10, pady=15)
        # Make interior data label
        self.interior = tk.Label(self, text="68\u00B0\n51\u00B0")
        self.interior.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.interior.config(fg="white", bg="grey8", font=self.dash_font,
                            padx=10, pady=15)
        # Make NWS synopsis label
        self.synopsis = tk.Label(self, text=" ")
        self.synopsis.pack(side=tk.LEFT, fill=tk.BOTH)
        self.synopsis.config(fg="white", bg="grey16", 
                            font= (self.dash_font[0], int(self.dash_font[1]/2.)),
                            padx=10, pady=10, wraplength=1000)
        self.update_synopsis( parent )
        
    def update_clock( self ):
        string = strftime("%a, %d %b %Y\n%H:%M:%S")
        self.clock.config(text = string)
        self.clock.after(1000, self.update_clock)
        
    def update_riseset( self, parent ):
        # Only retrieve data on initializaiton or if it's midnight
        if parent.init or strftime("%H") == "00":
            sr, ss = get_riseset()
            string = "%s \u25b2\n%s \u25bc" % (sr, ss)
            self.riseset.config(text = string)
        # Update every 30 minutes
        self.riseset.after(1800000, self.update_riseset)
        
    def update_synopsis( self, parent ):
        # Get standard and marine synopses from NWS
        synops, marine = get_synopsis()
        content = marine if parent.pages[parent.current_page] == 'Pacific' else synops
        multiplier = 0.55 * (1. - len(content)/2700.)
        self.synopsis.config(text = content, font=(self.dash_font[0], int(self.dash_font[1]*multiplier)))
        self.synopsis.after(1800000, self.update_synopsis)
        

if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()
