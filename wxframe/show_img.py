"""

Shows images in app

"""

import tkinter as tk
from PIL import Image, ImageTk


def show_img( path, xx=0, yy=0 ):
    
    # Create a photoimage object of the image in the path
    image = Image.open(path)
    test = ImageTk.PhotoImage(image)
    
    label = tk.Label(image=test)
    label.image = test
    
    # Position image
    label.place(anchor='center', x=xx, y=yy)
    #label.pack()






