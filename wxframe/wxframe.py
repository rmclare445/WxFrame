"""

Weather Frame driver script

Page 1 - Dashboard, pertinent locaL information
Page 2,3,.. - What's going on around the country/world

## should add tides to dashboard

## should make dashboard configuration a function

## add current conditions to dash (outdoor/indoor temp, hum)

## integrate with thermostat and ESP-2866 weather station

## update cycles every minute but with specific time conditionals

## when page is on "Pacific," switch synopsis to .MARINE. section of page

"""

import tkinter as tk
#from tkinter  import ttk
from get_img  import *
from riseset  import get_riseset
from nws_read import get_synopsis
from time     import strftime


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
        # Exit on Esc
        self.bind( "<Escape>", lambda x: self.destroy() )
        # Turn page on Enter ## will be amended to GPIO input on Pi
        self.bind( "<Return>", lambda x: self.turn_page() )
        
        # Get screen resources
        self.width  = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        # Get new images
        print("Getting updated images")
        #get_imgs()
        print("Updated images retrieved")
        
        # Establish pages
        self.pages = ['Local', 'CONUS', 'Pacific', 'Global', 'Forecast']
        
        # Make header with page name
        self.header = tk.Frame( self, relief=tk.RAISED, borderwidth=4 )
        self.header.place(relx=0, rely=0, anchor="nw")
        self.headtext = tk.Label( self.header, text="Local" )
        self.headtext.pack( )
        self.headtext.config(fg="white", bg="black", 
                             font=(self.globfont, int(self.height/36.), 'italic'),
                             padx=10, pady=5)
        self.current_page = 0
        
        #                             #
        #   Dashboard configuration   #
        #  _________________________  #
        self.dash = tk.Frame( self, relief=tk.RAISED, borderwidth=4 )
        self.dash.place(relx=0, rely=1, anchor="sw")
        self.dash_font = (self.globfont, int(self.height/36.), 'bold')
        # Make clock
        self.clock = tk.Label(self.dash, text="")
        self.clock.pack(side=tk.LEFT, fill=tk.BOTH)
        self.clock.config(fg="white", bg="navy", font=self.dash_font,
                          padx=20, pady=15)
        # Make sunrise/set label
        self.riseset = tk.Label(self.dash, text="")
        self.riseset.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.riseset.config(fg="white", bg="red", font=self.dash_font,
                            padx=20, pady=15)
        # Make exterior data label
        self.exterior = tk.Label(self.dash, text="52\u00B0\n31\u00B0")
        self.exterior.pack(side=tk.LEFT, fill=tk.BOTH)
        self.exterior.config(fg="white", bg="grey2", font=self.dash_font,
                            padx=20, pady=15)
        # Make interior data label
        self.interior = tk.Label(self.dash, text="68\u00B0\n51\u00B0")
        self.interior.pack(side=tk.LEFT, fill=tk.BOTH, padx=1)
        self.interior.config(fg="white", bg="grey8", font=self.dash_font,
                            padx=20, pady=15)
        # Make NWS synopsis label
        self.synopsis = tk.Label(self.dash, text=" ")
        self.synopsis.pack(side=tk.LEFT, fill=tk.BOTH)
        self.synopsis.config(fg="white", bg="grey16", 
                            font= (self.dash_font[0], int(self.dash_font[1]/2.)),
                            padx=20, pady=10, wraplength=1000)
        
        # #                             #
        # #     Body configuration      # ## might be a huge mistake
        # #  _________________________  #
        # self.body = tk.Frame( self )
        # self.body.place(relx=0.5, rely=0.4, anchor="center")
        # #
        # self.pic = tk.Label( self.body, image=pw_conus_maxtemp[1])
        # self.pic.place()
        
        # Display image
        show_img( nws_meteogram[1], .3, .4 )
        
        # Initialize update cycles
        self.update_clock()
        self.update_riseset()
        self.update_synopsis()
        
        # Initialization period over
        self.init = False
        
    def update_clock( self ):
        string = strftime("%a, %d %b %Y\n%H:%M:%S")
        self.clock.config(text = string)
        self.clock.after(1000, self.update_clock)
        
    def update_riseset( self ):
        # Only retrieve data on initializaiton or if it's midnight
        if self.init or strftime("%H") == "00":
            self.sr, self.ss = get_riseset()
            string = "%s \u25b2\n%s \u25bc" % (self.sr, self.ss)
            self.riseset.config(text = string)
        # Update every 30 minutes
        self.riseset.after(1800000, self.update_riseset)
        
    def update_synopsis( self ):
        synops, marine = get_synopsis()
        if self.pages[self.current_page] == 'Pacific':
            self.synopsis.config(text = marine, font=(self.dash_font[0], int(5*self.dash_font[1]/12.)))
        else:
            self.synopsis.config(text = synops, font=(self.dash_font[0], int(self.dash_font[1]/2.)))
        self.synopsis.after(1800000, self.update_synopsis)
        
    def turn_page( self ):
        #
        if self.current_page < 4:
            self.current_page+=1
        else:
            self.current_page = 0
        self.headtext.config(text = self.pages[self.current_page])
        self.update_synopsis()


if __name__ == "__main__":
    app = WxFrame()
    app.mainloop()
