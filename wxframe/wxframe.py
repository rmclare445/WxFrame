"""

Weather Frame driver script

"""

import tkinter as tk
#from tkinter import ttk
from clock import clock
        


class WxFrame( tk.Tk ):
    def __init__( self ):
        super().__init__()
        
        self.title("WxFrame")
        self.configure(bg='black')
        self.attributes('-fullscreen', True)
        
        # Exit on Esc
        self.bind( "<Escape>", lambda x: self.destroy() )

        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Make clock        
        frame = clock(tk.Frame(self), self)
        frame.update()


if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()