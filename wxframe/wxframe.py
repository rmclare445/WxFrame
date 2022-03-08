"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

"""

import tkinter as tk
#from tkinter import ttk
from clock   import clock
#from get_img import get_imgs
from get_img import *
from show_img import show_img


class WxFrame( tk.Tk ):
    def __init__( self ):
        super().__init__()
        
        # Configure attributes
        self.title("WxFrame")
        self.configure(bg='black')
        self.attributes('-fullscreen', True)
        
        # Exit on Esc
        self.bind( "<Escape>", lambda x: self.destroy() )

        # Get screen resources
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Make clock        
        frame = clock(tk.Frame(self), self)
        frame.update()
        
        # Get new images
        print("Getting updated images")
        get_imgs()
        
        # Display image
        show_img( nws_meteogram[1], self.width/2, self.height/2 )


if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()