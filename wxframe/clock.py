import tkinter as tk
from tkinter import ttk
from time import strftime

class clock( tk.Frame ):
    def __init__(self, parent, controller):
        clk = tk.Frame.__init__(self, master=parent)
        
        self.lbl = ttk.Label(clk, font = ('calibri', 150, 'bold'),
                             background = 'black', foreground = 'white')
        self.lbl.place(anchor='sw', x=0, y=controller.height)
        
    def update( self ):
        string = strftime('%H:%M:%S')
        self.lbl.config(text = string)
        self.lbl.after(1000, self.update)