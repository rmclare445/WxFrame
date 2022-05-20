"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

## should add tides to dashboard (or tide table to marine page)

## combine goes.py and nexrad.py into one module?

## integrate with thermostat and ESP-2866 weather station

## update cycles every minute but with specific time conditionals?

## updates should be managed by a separate block of function(s) in a new file which ingest the WxFrame as a parent

## Potentially, updates could be handled by wget scripts?  It would be easy to command a backgorund process on linux

## make a function that slowly cycles randomly thru pages

## add a print screen funciton bound to some key on the number pad

## add a force refresh button?

## def halfhour_update( parent ):
##    parent.thing.update()

## Honestly, should do much of the data analysis and plot rendering locally.
##  Make better plots with local times and my preferences
##  Much better long-term stability as websites change
##  This is an undertaking which will take much time and be done gradually

"""

#import threading
import platform
import tkinter as tk
import pages   as pg
import goes, nexrad
from dashboard import Dashboard
from get_img   import get_imgs


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
        # Turn page on Enter (For conventional and Macally inputs)
        self.bind( "<Return>",   lambda x: self.turn_page() )
        self.bind( "<KP_Enter>", lambda x: self.turn_page() )
        # Bind all the number keys to toggle pages by number
        for i in range(10):
           self.bind( str(i),            self.toggle_page)
           self.bind( '<KP_'+str(i)+">", self.toggle_page)
           
        # Bind animation controls
        self.bind( "<asterisk>",    lambda x: self.pause() )
        self.bind( "<KP_Multiply>", lambda x: self.pause() )
        self.paused = False
        self.bind( "-",             lambda x: self.minus() )
        self.bind( "<KP_Subtract>", lambda x: self.minus() )
        self.bind( "+",             lambda x: self.plus()  )
        self.bind( "<KP_Add>",      lambda x: self.plus()  )
        self.anim_wait = 100
        
        # KP_Decimal, KP_Divide, equal, BackSpace
        
        # Get screen resources
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        #
        self.goes_update = False
        self.nexrad_update = False
        
        # Get new images
        print("Getting updated images")
        #get_imgs()
        #nexrad.get_nexrad(self)
        #goes.get_goes(self)
        #self.update_15min()
        print("Updated images retrieved")
        
        # Initialize pages, show homepage
        self.ps  = [ pg.Page00(self),
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
            self.ps[self.current_page].cycle()
        else:
            # Decrease wait time between frames
            self.anim_wait = max(10, self.anim_wait-30)
        
    def minus( self ):
        ''' Animation control '''
        if self.paused and type(self.ps[self.current_page]).__name__ == "FullAnimPage":
            # Single frame retreat when paused
            self.ps[self.current_page].advance( -1 )
            self.ps[self.current_page].cycle()
        else:
            # Increase wait time between frames
            self.anim_wait = min(500, self.anim_wait+30)
        
    # def update_15min( self ):
    #     threading.Thread(target=self.thread_test).start()
    #     #self.after(900000, self.update_15min)
    #     self.after(60000, self.update_15min)
        
    # def thread_test( self ):
    #     # self.status_dialogue( 'UPDATING...' )
    #     nexrad.get_nexrad( self )
    #     #goes.get_goes( self )
    #     # self.rm_status_dialogue()


if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()
    ## GPIO cleanup for RPi