"""

WxFrame pages defined

## Need to add update functions to pages

## Should have a Sierra snow forecast page

## Maybe add a California fire monitoring page?

## Non-weather page (news / stocks?)

## The Pivotal and the Bentley maps both have associated forecasts
##  on the same plots.  The QuadPlotPages could toggle through times
##  by using +/-

"""

import tkinter as tk
import buoy
from get_img  import *
from nws_read import get_wrh, get_discussion, get_marine


class UserHomePage( tk.Frame ):
    ''' Home page showing local forecast informations '''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = 'Local Forecast'
        
    def show( self ):
        # Home NOAA Meteogram
        self.longmet = tk.Frame( self.parent )
        self.longmet.place(relx=0, rely=0.88, anchor="sw")
        img = Image.open(upd_dir+"meteogram.png")
        resized = img.crop((270, 35, 2200, 485))
        self.met00 = ImageTk.PhotoImage( resized )
        self.homemet00 = tk.Label(self.longmet, image=self.met00, borderwidth=0)
        self.homemet00.pack(side=tk.LEFT, fill=tk.BOTH)

        # Western Regional text forecast for Monterey / Big Sur
        w = get_wrh()
        self.wrh = tk.Frame( self.parent, relief=tk.RAISED, borderwidth=2 )
        self.wrh.place(relx=0., rely=0.06, anchor='nw')
        self.wrhlabel = tk.Label( self.wrh, text=w, height=23, anchor='nw', justify=tk.LEFT )
        self.wrhlabel.pack( )
        self.wrhlabel.config(fg="white", bg="black", 
                                  font=('arial black', int(self.parent.height/110)),
                                  padx=5, pady=4, wraplength=600)

        # Make NWS discussion frame
        d = get_discussion()
        try:
            textdiv = 90. if len(d) < 2300 else 100.
        except:
            d = 'No discussion right now.'
            textdiv = 90.
        self.discussion = tk.Frame( self.parent, relief=tk.RAISED, borderwidth=2 )
        self.discussion.place(relx=0.99, rely=0.06, anchor='ne')
        self.discusslabel = tk.Label( self.discussion, text=d, height=22, anchor='nw', 
                                      justify=tk.LEFT )
        self.discusslabel.pack( )
        self.discusslabel.config(fg="white", bg="black", 
                                  font=('lucida', int(self.parent.height/textdiv)),#90.)),
                                  padx=10, pady=4, wraplength=1250)
        self.refresh()
        
    def refresh( self ):
        img = Image.open(upd_dir+"meteogram.png")
        resized = img.crop((270, 35, 2200, 485))
        self.met00 = ImageTk.PhotoImage( resized )
        self.homemet00.config( image=self.met00 )
        self.wrhlabel.config( text=get_wrh() )
        self.discusslabel.config( text=get_discussion() )
        self.homemet00.after(60000, self.refresh)

    def disappear( self ):
        self.longmet.destroy()
        self.wrh.destroy()
        self.discussion.destroy()


class MarineCAPage( tk.Frame ):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.name = 'Marine'
        self.parent = parent
        
    def show( self ):
        # Surfline SST plot, resized to ~ 2/3
        img = Image.open(surfline_sst[1])
        resized = img.resize((644, 397),Image.ANTIALIAS)
        cropped = resized.crop((0, 0, 460, 397))
        self.SST = ImageTk.PhotoImage(cropped)
        self.sst = tk.Label(image=self.SST)
        self.sst.place(anchor='nw', relx=0., rely=0.09)
        # Surfline WND plot, resized to ~ 2/3
        img = Image.open(surfline_wnd[1])
        resized = img.resize((644, 397),Image.ANTIALIAS)
        cropped = resized.crop((0, 0, 460, 397))
        self.WND = ImageTk.PhotoImage(cropped)
        self.wnd = tk.Label(image=self.WND)
        self.wnd.place(anchor='nw', relx=0., rely=0.48)
        # CDIP swell map, cropped
        img = Image.open(cdip_swell[1])
        cropped = img.crop((60, 105, 580, 790))
        self.CDIP = ImageTk.PhotoImage(cropped)
        self.cdip = tk.Label(image=self.CDIP)
        self.cdip.place(anchor='nw', relx=0.26, rely=0.214)
        # Buoy table
        self.parent.tab = buoy.BuoyTable(self.parent)
        self.parent.tab.place(anchor='nw', relx=0.55, rely=0.45)
        # Buoy map
        img = Image.open(img_dir+"ndbc_map.png")
        cropped = img.crop((0, 50, 750, 240))
        darker  = cropped.point(lambda p: p * 0.7)  ## Need to do this outside of wxframe, no reason it can't be pre-done
        self.NDBC = ImageTk.PhotoImage(darker)
        self.ndbc = tk.Label(image=self.NDBC)
        self.ndbc.place(anchor='nw', relx=0.55, rely=0.214)
        # Marine synopsis
        self.marine = tk.Frame( self.parent, relief=tk.RAISED, borderwidth=2 )
        self.marine.place(relx=0.26, rely=0.09, anchor='nw')
        self.marinelabel = tk.Label( self.marine, text=get_marine(), justify=tk.LEFT, height=5 )
        self.marinelabel.pack( )
        self.marinelabel.config(fg="white", bg="midnight blue", 
                                font=('lucida', int(self.parent.height/75.)),
                                padx=15, pady=3, wraplength=1300)
        self.refresh()
    
    def refresh( self ):
        # Surfline SST plot, resized to ~ 2/3
        img = Image.open(surfline_sst[1])
        resized = img.resize((644, 397),Image.ANTIALIAS)
        cropped = resized.crop((0, 0, 460, 397))
        self.SST = ImageTk.PhotoImage(cropped)
        self.sst.config(image=self.SST)
        # Surfline WND plot, resized to ~ 2/3
        img = Image.open(surfline_wnd[1])
        resized = img.resize((644, 397),Image.ANTIALIAS)
        cropped = resized.crop((0, 0, 460, 397))
        self.WND = ImageTk.PhotoImage(cropped)
        self.wnd.config(image=self.WND)
        # CDIP swell map, cropped
        img = Image.open(cdip_swell[1])
        cropped = img.crop((60, 105, 580, 790))
        self.CDIP = ImageTk.PhotoImage(cropped)
        self.cdip.config(image=self.CDIP)
        # Buoy table
        self.parent.tab.destroy()
        self.parent.tab = buoy.BuoyTable(self.parent)
        self.parent.tab.place(anchor='nw', relx=0.55, rely=0.45)
        # Marine synopsis
        self.marinelabel.config(text=get_marine())
        self.marinelabel.after(60000, self.refresh)
        
    def disappear( self ):
        self.cdip.destroy()
        self.sst.destroy()
        self.wnd.destroy()
        self.parent.tab.destroy()
        self.ndbc.destroy()
        self.marine.destroy()
        
        
class FullAnimPage( tk.Frame ):
    ''' Displays a single image frame and refreshes images in a cycle to animate '''
    def __init__(self, parent, page ):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = page.name
        self.loc  = page.loc
        self.lst  = page.lst
        self.cdir = page.cdir
        self.c    = 0
    
    def disp( self ):
        self.frame = ImageTk.PhotoImage( Image.open(self.loc+self.lst[self.cdir*self.c]) )
        self.label = tk.Label(image=self.frame)
        self.label.place(anchor='center', relx=0.5, rely=0.44)
        self.parent.header.tkraise()
        
    def show( self ):
        self.disp()
        self.cycle()
        
    def disappear( self ):
        self.label.destroy()
        
    def advance( self, direction ):
        # Advances forward or backward one frame depending on direction (-1, 1)
        if direction == 1 and self.c == (len(self.lst)-1):
            self.c = 0
        elif direction == -1 and self.c == 0:
            self.c = (len(self.lst)-1)
        else:
            self.c = self.c + 1 * direction
        self.frame = ImageTk.PhotoImage( Image.open(self.loc+self.lst[self.cdir*self.c]) )
        self.label.config(image=self.frame)
        
    def cycle( self ):
        if not self.parent.paused:
            self.advance( 1 )
        self.label.after(self.parent.anim_wait, self.cycle)


class QuadPlotPage( tk.Frame ):
    ''' Displays four images attached at the center '''
    def __init__(self, parent, name):
        tk.Frame.__init__(self, parent)
        self.parent  = parent
        self.name    = name
        self.centerx = 0.59
        self.centery = 0.5
        if name == "CONUS Daily":
            self.images  = images[:4]
            self.centerx = 0.6
            self.xscale  = 0.68
            self.yscale  = 0.63
        elif name == "CONUS Analysis":
            self.images  = images[4:8]
            self.xscale  = 0.75
            self.yscale  = 0.68
        elif name == "Pacific Analysis":
            self.images  = images[8:12]
            self.xscale  = 0.75
            self.yscale  = 0.68
        
    def show( self ):
        self.parent.dash.trim()
        # Top Left Image
        img = Image.open(self.images[0][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.TLI = ImageTk.PhotoImage(resized)
        self.tli = tk.Label(image=self.TLI)
        self.tli.place(anchor='se', relx=self.centerx, rely=self.centery)
        # Top Right Image
        img = Image.open(self.images[1][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.TRI = ImageTk.PhotoImage(resized)
        self.tri = tk.Label(image=self.TRI)
        self.tri.place(anchor='sw', relx=self.centerx, rely=self.centery)
        # Bottom Left Image
        img = Image.open(self.images[2][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.BLI = ImageTk.PhotoImage(resized)
        self.bli = tk.Label(image=self.BLI)
        self.bli.place(anchor='ne', relx=self.centerx, rely=self.centery)
        # Bottom Right Image
        img = Image.open(self.images[3][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.BRI = ImageTk.PhotoImage(resized)
        self.bri = tk.Label(image=self.BRI)
        self.bri.place(anchor='nw', relx=self.centerx, rely=self.centery)
        
        self.refresh()
        
    def refresh( self ):
        img = Image.open(self.images[0][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.TLI = ImageTk.PhotoImage(resized)
        self.tli.config(image=self.TLI)
        img = Image.open(self.images[1][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.TRI = ImageTk.PhotoImage(resized)
        self.tri.config(image=self.TRI)
        img = Image.open(self.images[2][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.BLI = ImageTk.PhotoImage(resized)
        self.bli.config(image=self.BLI)
        img = Image.open(self.images[3][1])
        width, height = img.size
        resized = img.resize((int(width*self.xscale), int(height*self.yscale)),Image.ANTIALIAS)
        self.BRI = ImageTk.PhotoImage(resized)
        self.bri.config(image=self.BRI)
        self.bri.after(60000, self.refresh)
        
    def disappear( self ):
        self.tli.destroy()
        self.tri.destroy()
        self.bli.destroy()
        self.bri.destroy()
        self.parent.dash.show()