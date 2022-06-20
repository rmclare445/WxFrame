"""

Weather Frame driver script

## Must try to toggle pages without destroying labels, try pack() and forget_pack()

## should add tides to dashboard (or tide table to marine page)

## integrate with thermostat and ESP-2866 weather station

## make a function that slowly cycles randomly thru pages

## add a force refresh button?

## Honestly, should do much of the data analysis and plot rendering locally.
##  Make better plots with local times and my preferences
##  Much better long-term stability as websites change
##  This is an undertaking which will take much time and be done gradually

"""

import time, platform
import tkinter as tk
import pages   as pg
import goes, nexrad
from dashboard import Dashboard
from tools.system_tools import get_dirs_from_file
from get_img   import get_imgs, ImageGrab


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
        
        # Get local directory information
        #self.wrkdir, self.repo_dir = get_dirs_from_file(__file__)
        
        # Exit on Esc
        self.bind( "<Escape>",   lambda x: self.destroy()   )
        # Turn page on Enter (For conventional and Macally inputs)
        self.bind( "<Return>",   lambda x: self.turn_page() )
        self.bind( "<KP_Enter>", lambda x: self.turn_page() )
        # Bind all the number keys to toggle pages by number
        for i in range(10):
           self.bind( str(i),            self.toggle_page   )
           self.bind( '<KP_'+str(i)+">", self.toggle_page   )
           
        # Bind animation controls and set initial conditions
        self.bind( "<asterisk>",    lambda x: self.pause()  )
        self.bind( "<KP_Multiply>", lambda x: self.pause()  )
        self.paused = False
        self.bind( "-",             lambda x: self.minus()  )
        self.bind( "<KP_Subtract>", lambda x: self.minus()  )
        self.bind( "+",             lambda x: self.plus()   )
        self.bind( "<KP_Add>",      lambda x: self.plus()   )
        self.anim_wait = 100
        
        # Take screenshot on "="
        self.bind( "<equal>", lambda x: self.screenshot() )
        
        # There's also KP_Decimal, KP_Divide, BackSpace
        
        # Get screen resources
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Update booleans for pausing animations during updating
        self.goes_update = False
        self.nexrad_update = False
        
        # Get new images
        print("Getting updated images")
        get_imgs()
        nexrad.get_nexrad() #self)
        goes.get_goes() #self)
        print("Updated images retrieved")
        
        # Initialize pages, show homepage
        self.ps  = [ pg.UserHomePage(self),
                     pg.MarineCAPage(self),
                     pg.FullAnimPage(self, nexrad),
                     pg.FullAnimPage(self, goes),
                     pg.QuadPlotPage(self, "CONUS Daily"),
                     pg.QuadPlotPage(self, "CONUS Analysis"),
                     pg.QuadPlotPage(self, "Pacific Analysis") ]
        self.ps[0].show()
        
        # Display dashboard
        self.dash = Dashboard(self)
        
        # Make header with page name
        self.header = tk.Frame( self, relief=tk.RAISED, borderwidth=4 )
        self.header.place(relx=0, rely=0, anchor="nw")
        self.headtext = tk.Label( self.header, text="" )
        self.headtext.pack( )
        self.headtext.config(fg="white", bg="black", 
                             font=(self.globfont, int(self.height/36.), 'italic'),
                             padx=10, pady=5)
        self.headtext.config(text = self.ps[0].name)
        
        # Initialization period over
        self.init = False

    def toggle_page( self, n ):
        ''' Select page from numerical input (n) '''
        # Don't do anything if number input out of bounds
        if int(n.char) >= len(self.ps):
            return
        self.ps[self.current_page].disappear()
        self.paused = False
        self.anim_wait = 100
        self.current_page = int(n.char)
        self.headtext.config(text = self.ps[self.current_page].name)
        self.ps[self.current_page].show()
        
    def turn_page( self ):
        ''' Advance to the next page in self.ps, wrap around at the end '''
        self.ps[self.current_page].disappear()
        if self.current_page < len(self.ps)-1:
            self.current_page+=1
        else:
            self.current_page = 0
        self.headtext.config(text = self.ps[self.current_page].name)
        self.ps[self.current_page].show()
        
    def status_dialogue( self, string ):
        self.status = tk.Frame( self )
        self.status.place(relx=1, rely=0, anchor='ne')
        self.statuslabel = tk.Label( self.status, text=string )
        self.statuslabel.pack()
        self.statuslabel.config(fg="red", bg="black", 
                              font=('calibri light', int(self.height/36.), 'italic'),
                              padx=10, pady=5)
        self.statuslabel.update()
        
    def rm_status_dialogue( self ):
        self.status.destroy()

    def pause( self ):
        ''' Pause animations '''
        if type(self.ps[self.current_page]).__name__ == "FullAnimPage":
            self.paused = not self.paused

    def plus( self ):
        ''' Animation control '''
        if self.paused and type(self.ps[self.current_page]).__name__ == "FullAnimPage":
            # Single frame advance when paused
            self.ps[self.current_page].advance( 1 )
        else:
            # Decrease wait time between frames
            self.anim_wait = max(10, self.anim_wait-30)

    def minus( self ):
        ''' Animation control '''
        if self.paused and type(self.ps[self.current_page]).__name__ == "FullAnimPage":
            # Single frame retreat when paused
            self.ps[self.current_page].advance( -1 )
        else:
            # Increase wait time between frames
            self.anim_wait = min(500, self.anim_wait+30)
            
    def screenshot( self ):
        self.status_dialogue( "Saving screenshot...")
        ImageGrab.grab().save( "screenshots/"+time.strftime("%Y%m%d%H%M%S")+".png" )
        time.sleep(1)
        self.rm_status_dialogue()


if __name__ == "__main__":
    # Detect if on Raspberry Pi (method works but less than ideal)
    rpi = True if platform.system() == "Linux" else False
    try:
        app = WxFrame()
        app.mainloop()
    finally:
        if rpi:
            ## GPIO cleanup for RPi
            pass
