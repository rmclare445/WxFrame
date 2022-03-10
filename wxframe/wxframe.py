"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

"""

import tkinter as tk
from tkinter  import ttk
from get_img  import *
from riseset  import get_riseset
from nws_read import get_synopsis
from time     import strftime


class WxFrame( tk.Tk ):
    def __init__( self ):
        super().__init__()
        
        # Configure attributes
        self.title("WxFrame")
        self.configure(bg='black')
        self.attributes('-fullscreen', True)
        #
        self.init = True
        
        # Exit on Esc
        self.bind( "<Escape>", lambda x: self.destroy() )
        
        # Get new images
        # print("Getting updated images")
        # get_imgs()
        
        #                             #
        #   Dashboard configuration   #
        #  _________________________  #
        self.dash = tk.Frame( self, relief=tk.RAISED, borderwidth=4 )
        self.dash.place(relx=0, rely=1, anchor="sw")
        self.dash_font = ('lucida', 40, 'bold')
        # Make clock
        self.clock = tk.Label(self.dash, text="")
        self.clock.pack(side=tk.LEFT, fill=tk.BOTH)
        self.clock.config(fg="white", bg="navy", font=self.dash_font,
                          padx=20, pady=15)
        # Show sun rise/set times
        self.riseset = tk.Label(self.dash, text="")
        self.riseset.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.riseset.config(fg="white", bg="red", font=self.dash_font,
                            padx=30, pady=15)
        # Show NWS synopsis
        self.synopsis = tk.Label(self.dash, text=" ")
        self.synopsis.pack(side=tk.LEFT, fill=tk.BOTH)
        self.synopsis.config(fg="white", bg="grey16", 
                            font= (self.dash_font[0], 15),
                            padx=20, pady=10)
        
        
        # Display image
        show_img( nws_meteogram[1], .3, .4 )
        
        #
        self.update_clock()
        self.update_riseset()
        self.update_synopsis()
        
        #
        self.init = False
        
    def update_clock( self ):
        string = strftime("%a, %d %b %Y\n%H:%M:%S")
        self.clock.config(text = string)
        self.clock.after(1000, self.update_clock)
        
    def update_riseset( self ):
        # Only retrieve data on startup or if it's midnight
        if self.init == True or strftime("%H") == "00":
            self.sr, self.ss = get_riseset()
            string = "%s \u25b2\n%s \u25bc" % (self.sr, self.ss)
            self.riseset.config(text = string)
        # Update every 59 minutes
        self.riseset.after(3540000, self.update_riseset)
        
    def update_synopsis( self ):
        string = get_synopsis()
        self.synopsis.config(text = string)
        self.synopsis.after(3600000, self.update_synopsis)


if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()