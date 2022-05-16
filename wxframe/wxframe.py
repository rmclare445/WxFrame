"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

## should add tides to dashboard (or tide table to marine page)

## combine goes.py and nexrad.py into one module

## integrate with thermostat and ESP-2866 weather station

## update cycles every minute but with specific time conditionals

## updates should be managed by a separate block of function(s) in a new file which ingest the WxFrame as a parent

## Potentially, updates could be handled by wget scripts?  It would be easy to command a backgorund process on linux

## make a function that slowly cycles randomly thru pages

## add a print screen funciton bound to some key on the number pad

## add a force refresh button?

## should synopsis move from dash to page?

## def halfhour_update( parent ):
##    parent.thing.update()

## Honestly, should do much of the data analysis and plot rendering locally.
##  Make better plots with local times and my preferences
##  Much better long-term stability as websites change
##  This is an undertaking which will take much time and be done gradually

"""

#import threading
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
        # Turn page on Enter ## will be amended to GPIO input on Pi
        #self.bind( "<Return>", lambda x: self.turn_page() )
        # Bind all the number keys to toggle pages by number
        for i in range(10):
           self.bind(str(i), self.toggle_page)
        # Bind asterisk to pause animations
        self.bind( "<*>", lambda x: self.pause() )
        self.paused = False
        # Animation speed controls
        self.bind( "-", lambda x: self.slower() )
        self.bind( "+", lambda x: self.faster() )
        self.anim_wait = 100
        
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
        self.p00 = pg.Page00(self)
        self.p01 = pg.MarineCAPage(self)
        self.p02 = pg.FullAnimPage(self, nexrad)
        self.p03 = pg.FullAnimPage(self, goes)
        self.p04 = pg.QuadPlotPage(self, "CONUS Daily")
        self.p05 = pg.QuadPlotPage(self, "CONUS Analysis")
        self.p06 = pg.QuadPlotPage(self, "Pacific Analysis")
        self.ps  = [self.p00, self.p01, self.p02, self.p03, self.p04, self.p05, self.p06]
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
        #self.dash.update_synopsis( self )
        self.headtext.config(text = self.ps[self.current_page].name)
        self.ps[self.current_page].show()
        #self.dash.tkraise()
        
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
            
    def faster( self ):
        ''' Decrease wait time between frames '''
        self.anim_wait = max(10, self.anim_wait-30)
        
    def slower( self ):
        ''' Increase wait time between frames '''
        self.anim_wait = min(500, self.anim_wait+30)
        
    # def turn_page( self ):
    #     #
    #     self.ps[self.current_page].disappear()
    #     if self.current_page < 2:
    #         self.current_page+=1
    #     else:
    #         self.current_page = 0
    #     self.headtext.config(text = self.ps[self.current_page].name)
    #     # self.dash.update_synopsis( self )
    #     #self.current_page = abs( self.current_page - 1 )
    #     self.ps[self.current_page].show()
        
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