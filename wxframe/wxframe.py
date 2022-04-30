"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

## should add tides to dashboard

## buoy table on Pacific page

## combine goes.py and nexrad.py into one module

## combine Page02 and Page03 into one class

## integrate with thermostat and ESP-2866 weather station

## update cycles every minute but with specific time conditionals

## updates should be managed by a separate block of function(s) in a new file which ingest the WxFrame as a parent

"""

import tkinter as tk
import pages   as pg
from dashboard import Dashboard
from nexrad    import get_nexrad
from goes      import get_goes


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
        # Bind all the number keys with the callback function
        for i in range(10):
           self.bind(str(i), self.toggle_page)
        
        # Get screen resources
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Get new images
        print("Getting updated images")
        #get_imgs()
        #get_nexrad()
        #get_goes()
        print("Updated images retrieved")
        
        # Initialize pages
        self.p00 = pg.Page00(self)
        self.p01 = pg.Page01(self)
        self.p02 = pg.Page02(self)
        self.p03 = pg.Page03(self)
        self.ps  = [self.p00, self.p01, self.p02, self.p03]
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

    def toggle_page( self, n ):
        # Select page from numerical input (n)
        self.ps[self.current_page].disappear()
        self.current_page = int(n.char)
        self.dash.update_synopsis( self )
        self.headtext.config(text = self.ps[self.current_page].name)
        self.ps[self.current_page].show()
        #self.header.tkraise()
        

if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()
    ## GPIO cleanup for RPi