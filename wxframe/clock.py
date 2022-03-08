"""

Responsible for clock functions on the Weather Frame

"""

import tkinter as tk
from tkinter import ttk
from time import strftime

class clock( tk.Frame ):
    def __init__(self, parent, controller): ## should add positional/aesthetic kwarg(s)?
        clk = tk.Frame.__init__(self, master=parent)
        
        self.lbl = ttk.Label(clk, font = ('lucida', 90, 'bold'),
                              background = 'navy', foreground = 'white',
                              #borderwidth=10, relief=tk.RAISED,  # uncommenting this shows border
                              padding=30)
        self.lbl.place(anchor='sw', x=0, y=controller.height)
        
    def update( self ):
        string = strftime('%H:%M:%S')
        self.lbl.config(text = string)
        self.lbl.after(1000, self.update)