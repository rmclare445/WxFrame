"""

WxFrame dashboard

"""

import tkinter as tk
from riseset  import get_riseset
from nws_read import get_synopsis
from time     import strftime
from thermopi import get_temps


class Dashboard( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief=tk.RAISED, borderwidth=4 )
        self.parent = parent
        self.place(relx=0, rely=1, anchor="sw")
        self.dash_font = (parent.globfont, int(parent.height/40.), 'bold')
        
        # Make clock
        self.clock = tk.Label(self, text="")
        self.clock.pack(side=tk.LEFT, fill=tk.BOTH)
        self.clock.config(fg="white", bg="navy", font=self.dash_font,
                          padx=20, pady=15)
        self.update_clock( )
        self.full = False
        
        self.show()
        
    def show( self ):
        # Guard against duplication
        if self.full:
            return
        # Make sunrise/set label
        self.riseset = tk.Label(self, text="")
        self.riseset.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.riseset.config(fg="white", bg="red", font=self.dash_font,
                            padx=10, pady=15)
        self.update_riseset( )
        self.riseset.config(text = self.suntimes)
        
        # Make exterior data label (dummy data for now)
        self.exterior = tk.Label(self, text="--\u00B0\n--\u00B0")
        self.exterior.pack(side=tk.LEFT, fill=tk.BOTH)
        self.exterior.config(fg="white", bg="grey2", font=self.dash_font,
                             padx=10, pady=15)
        # Make interior data label
        self.interior = tk.Label(self, text="%s\u00B0\n%s\u00B0" % get_temps())
        self.interior.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.interior.config(fg="white", bg="grey8", font=self.dash_font,
                             padx=10, pady=15)
        self.update_temps( )
        # Make NWS synopsis label
        self.synopsis = tk.Label(self, text=" ")
        self.synopsis.pack(side=tk.LEFT, fill=tk.BOTH)
        self.synopsis.config(fg="white", bg="grey16", 
                             font= (self.dash_font[0], int(self.dash_font[1]/2.)),
                             padx=10, pady=10, wraplength=1000)
        self.update_synopsis( )
        
        self.full = True
        
    def trim( self ):
        if self.full:
            self.riseset.destroy()
            self.exterior.destroy()
            self.interior.destroy()
            self.synopsis.destroy()
            self.full = False
        
    def update_clock( self ):
        string = strftime("%a, %d %b %Y\n%H:%M:%S")
        self.clock.config(text = string)
        self.clock.after(1000, self.update_clock)

    def update_temps( self ):
        self.interior.config(text="%s\u00B0\n%s\u00B0" % get_temps())
        self.interior.after(15000, self.update_temps)
        
    def update_riseset( self ):
        # Only retrieve data on initializaiton or if it's midnight
        if self.parent.init or strftime("%H") == "00":
            sr, ss = get_riseset()
            self.suntimes = "%s \u25b2\n%s \u25bc" % (sr, ss)
            #self.riseset.config(text = self.suntimes)
        # Update every 30 minutes
        self.riseset.after(1800000, self.update_riseset)
        
    def update_synopsis( self ):
        # Get synopses from NWS
        content = get_synopsis()
        multiplier = 0.55 * (1. - min(len(content)/2700., .9))
        self.synopsis.config(text = content, font=(self.dash_font[0], int(self.dash_font[1]*multiplier)))
        self.synopsis.after(1800000, self.update_synopsis)
