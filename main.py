import tkinter as tk
import math as m
from PIL import Image, ImageTk, ImageDraw
import random
from tkdial import *
import time

global screen
screen = 1
global prevScr
prevScr = 0
global directivesLn
directivesLn = -1
global lines
global mapOffset
mapOffset = (960, 650)

global azRad
global elRad
azRad = 0
elRad = 0
global muzzleVelocity
muzzleVelocity = 100
global gravity
gravity = 10


def rotatePolygon(angleDeg, points, offx, offy):#func to rotate a liste of points for drawing stuff at an angle
    points2 = [list(point) for point in points]
    dirRad = m.radians(angleDeg)
    cos = m.cos(dirRad)
    sin = m.sin(dirRad)
    for i in range(len(points2)):
        points2[i][0], points2[i][1] = int(points2[i][0]*cos - points2[i][1]*sin+offx), int(points2[i][0]*sin + points2[i][1]*cos+offy)
        
    return(points2)

def testClick(event):
    print(f"{event.x}, {event.y}")
    if screen == 1:
        game.recon(event.x, event.y, random.randint(-90,90))





class projectile:
    def __init__(self):
        groundSpeed = muzzleVelocity * m.cos(elRad)
        self.vz = muzzleVelocity * m.sin(elRad)
        self.vx = groundSpeed * m.sin(azRad)
        self.vy = groundSpeed * m.cos(azRad)
        self.x = 630
        self.y = 600
        self.z = 10
        self.tick()
        print(elRad, azRad)
        print(self.vz, self.vx, self.vy)
    def tick(self):
        self.x = self.x + self.vx
        self.y = self.y - self.vy
        self.z = self.z + self.vz
        self.vz = self.vz - gravity
        if self.z > 0:
            game.root.after(1000, self.tick)
        else:
            
            game.fullMap.paste(game.impact1, (int(self.x)+160, int(self.y)+150), mask=game.impact1)
            game.root.after(500, game.recon(int(self.x), int(self.y), 10))
        







class game:


    def nextMission(self):#plays next set of directives I think(haven't properly tested this yet)
        global directivesLn
        global lines
        directivesLn +=1
        game.directivesBox.insert("end", "---------------------------------------------------------------------\n")
        while(lines[directivesLn].strip()):
            game.directivesBox.insert("end", lines[directivesLn])
            directivesLn += 1

    def menuloop(self):
        global prevScr
        game.canvas.delete("gun")
        if screen ==1:
            if not prevScr == 1: #page 1 init
                game.mapdisplay = game.canvas.create_image(mapOffset[0],mapOffset[1],image=map_1, tags="map")#map display
                #change buttons to show what screen is up
                game.mapB1.config(bg="green", fg="black")
                game.mapB2.config(bg="grey", fg="black")
                game.mapB3.config(bg="grey", fg="black")

                game.canvas.itemconfigure(game.directivesBoxWindow, state="hidden")#change what windows are visible
                game.canvas.itemconfigure(game.crankE, state="hidden")
                game.canvas.itemconfigure(game.crankA, state="hidden")

        elif screen == 2:
            if not prevScr == 2:#page 2 init
                game.canvas.delete("map")
                #change buttons to show what screen is up
                game.mapB1.config(bg="grey", fg="black")
                game.mapB2.config(bg="green", fg="black")
                game.mapB3.config(bg="grey", fg="black")

                game.canvas.itemconfigure(game.directivesBoxWindow, state="normal")#change what windows are visible
                game.canvas.itemconfigure(game.crankE, state="hidden")
                game.canvas.itemconfigure(game.crankA, state="hidden")

        else:
            if not prevScr == 3:#page 3 init
                game.canvas.delete("map")
                #change buttons to show what screen is up
                game.mapB1.config(bg="grey", fg="black")
                game.mapB2.config(bg="grey", fg="black")
                game.mapB3.config(bg="green", fg="black")

                game.canvas.itemconfigure(game.directivesBoxWindow, state="hidden")#change what windows are visible
                game.canvas.itemconfigure(game.crankE, state="normal")
                game.canvas.itemconfigure(game.crankA, state="normal")

            #draw gun stuff
            gunPoints = ((-400,80),(-400,-80),(200,-80),(600,-50),(600,50),(200,80))#barrel points relative to turning point
            game.canvas.create_arc((1300, 000, 1900, 600,), fill="grey30", start=(game.knobE.get()/10)+220, extent=90, tags="gun")#trunion ring gear
            game.canvas.create_polygon(rotatePolygon((game.knobE.get()/-10),gunPoints, 1600, 300), fill="grey", tags="gun")#rotating barrel/chamber
            game.canvas.create_polygon(((0,800),(0,1000),(1920,1000),(1920,800),(1920,500),(1700,500),(1500,800)), fill="grey38", tags="gun")#elevation mechanism mount
            game.canvas.create_oval(1560,260, 1640,340, fill="grey30", tags="gun", outline="grey30")#circle

            if game.knobE:
                global elRad
                elRad = m.radians(game.knobE.get()/10)
            if game.knobA:
                global azRad
                azRad = m.radians(game.knobA.get()/10)

        prevScr = screen
        game.root.after(10, game.menuloop)

    def recon(ix, iy, dir):
        ix = ix
        iy = iy
        global map_1

        section = game.fullMap.convert("RGBA")
        section = section.crop((ix,iy,300+ix,300+iy))

        poly = Image.new("RGBA", (300, 300), color=(0,0,0,0))
        poly2 = ImageDraw.Draw(poly)

        points = ((-50,100),(50,100),(50,-100),(-50,-100))
        pointsR = rotatePolygon(dir, points, 200,200)
        poly2.polygon(pointsR, fill="orange")

        mask = poly.split()[3]
        #mask = mask.resize(section.size)
        game.blankMap.paste(section, (ix,iy), mask=mask)
        #blankMap.paste(mask, (ix,iy) )
        map_1 = ImageTk.PhotoImage(game.blankMap)
        game.mapdisplay = game.canvas.create_image(mapOffset[0],mapOffset[1],image=map_1, tags="map")#map display

    def shoot(self):
        projectile()
    #screen tab button
    def bone(self):
        global screen
        screen = 1
    def btwo(self):
        global screen
        screen = 2
    def bthree(self):
        global screen
        screen = 3

    def __init__(self):
        self.root = tk.Tk() #root window i think
        self.root.title("iron nest ripoff")#title
        self.root.geometry("1920x1080+0+0")

        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg="black")
        self.canvas.pack()




        #images
        self.fullMap = Image.open("greyscalemap.png")
        self.pixel = tk.PhotoImage(width=1, height=1)#invisible pixel for button sizing i guess
        #map displays
        self.blankMap = Image.new("RGBA", (1920, 1080), color=(0,0,0,0))
        self.map_1 = ImageTk.PhotoImage(self.blankMap)

        self.impact1 = Image.open("smallimpact.png")
        self.impact1 = self.impact1.convert("RGBA")


        #buttons for screen change
        self.mapB1 = tk.Button(self.root, text="Map", width=300, height=140, image=self.pixel,compound="left", command=self.bone, font=("arial", 40, "bold"))
        self.mapB2 = tk.Button(self.root, text="Directives", width=300, height=140, image=self.pixel,compound="left", command=self.btwo, font=("arial", 40, "bold"))
        self.mapB3 = tk.Button(self.root, text="Breach", width=300, height=140, image=self.pixel,compound="left", command=self.bthree, font=("arial", 40, "bold"))
        #other ones
        self.directivesBox = tk.Text(self.root, width=70, height=50)
        self.shootB = tk.Button(self.root, text="Fire", width=300, height=140, image=self.pixel,compound="left", command=self.shoot, bg="red", font=("arial", 40, "bold"))



        self.knobE = ImageKnob(self.root, image="handle.png", text_color="white",end=600, text="Elevation ", bg="grey38", start_angle=0,scale_width=70, end_angle=-7200, scroll_steps=1, radius=200, command=lambda: self.updateDial(self.knobE, "Elevation: "))

        self.knobA = ImageKnob(self.root, image="handle.png", text_color="white",start=-600, end=600, text="Azimuth ", bg="grey38", start_angle=18000,scale_width=70, end_angle=-18000, scroll_steps=1, radius=200, command=lambda: self.updateDial(self.knobA, "Azimuth: "))

        self.knobA.set(0)

        #summoning screen change buttons at start
        self.canvas.create_window(550, 80, window=self.mapB1)
        self.canvas.create_window(960, 80, window=self.mapB2)
        self.canvas.create_window(1370, 80, window=self.mapB3)

        #cranks and shoot
        self.crankE = self.canvas.create_window(1800, 600, window=self.knobE)
        self.crankA = self.canvas.create_window(1700, 800, window=self.knobA)
        self.canvas.create_window(1300, 900, window=self.shootB)

        #directives
        self.directivesBoxWindow = self.canvas.create_window(450, 550, window=self.directivesBox)
        with open("directives.txt", "r", encoding="utf-8") as file:
            self.lines = file.readlines()

        self.nextMission()

        self.recon(630, 600, 1)
        #loops or sum
        self.menuloop()
        self.root.mainloop()


    def updateDial(dial, text):
        dial.configure(text=f"{text}{dial.get()/10}°")



game()

"""
arrows to switch tabs
def larrow(self):
    game.screen
    if game.screen >=2:
        game.screen -=1
def rarrow(self):
    game.screen
    if game.screen <=2:
        game.screen +=1
#close the program with esc
def kill(self):
    game.root.destroy()
#keybinds
game.root.bind("<Escape>", kill)
game.root.bind("<Left>", larrow)
game.root.bind("<Right>", rarrow)

game.canvas.bind("<Button-1>", testClick)
"""