"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

"""

import tkinter as tk
from tkinter import ttk
#from clock   import Clock
from get_img import *
from time import strftime


class WxFrame( tk.Tk ):
    def __init__( self ):
        super().__init__()
        
        # Configure attributes
        self.title("WxFrame")
        self.configure(bg='black')
        self.attributes('-fullscreen', True)
        
        # Exit on Esc
        self.bind( "<Escape>", lambda x: self.destroy() )
        
        # Get new images
        print("Getting updated images")
        get_imgs()
        
        # Create dashboard
        self.dash = tk.Frame( self, relief=tk.RAISED, borderwidth=4 )
        self.dash.place(relx=0, rely=1, anchor="sw")
        
        # Make clock
        self.clock = tk.Label(self.dash, text="")
        self.clock.pack(side=tk.LEFT, fill=tk.BOTH)
        self.clock.config(fg="white", bg="navy", font=('lucida', 40, 'bold'),
                          padx=20, pady=15)
        # Show sun rise/set times
        self.riseset = tk.Label(self.dash, text="06:52 \u25b2\n18:58 \u25bc")
        self.riseset.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.riseset.config(fg="white", bg="grey3", font=('lucida', 40, 'bold'),
                          padx=30, pady=15)
        
        # Display image
        # show_img( nws_meteogram[1], self.width/2, self.height/2 )
        
        self.update_clock()
        
    def update_clock( self ):
        string = strftime("%a, %d %b %Y\n%H:%M:%S")
        self.clock.config(text = string)
        self.clock.after(1000, self.update_clock)


if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()