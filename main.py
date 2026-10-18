import tkinter as tk
import math as m
from PIL import Image, ImageTk, ImageDraw, ImageEnhance
import random
from tkdial import *


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
    if game.screen == 1:
        game.recon(event.x, event.y, random.randint(-90,90))

def updateDial(dial, text):
    dial.configure(text=text)

class projectile:
    def __init__(self, master, round):
        self.master = master #so i can use variables from game
        self.round = round
        groundSpeed = 100 * m.cos(self.master.elRad)#groundspeed
        self.vz = 100 * m.sin(self.master.elRad)#vertical speed for flight time
        self.vx = groundSpeed * m.sin(self.master.azRad)#x speed
        self.vy = groundSpeed * m.cos(self.master.azRad)#y speed
        self.x = 630#starting location of turret
        self.y = 600
        self.z = 10
        self.tick()#start flying
    def tick(self):
        self.x = self.x + self.vx/100#add velocities to map location
        self.y = self.y - self.vy/100
        self.z = self.z + self.vz/100
        self.vz = self.vz - 0.1
        self.master.screen = 1 #locks to map screen
        if self.z > 0:#if in air continue flying
            self.master.root.after(10, self.tick)
        else:#else impact
            if self.master.projectiles[self.round][1] == 1:
                            self.master.fullMap.paste(self.master.impact2, (int(self.x)+180, int(self.y)+180), mask=self.master.impact2.split()[3])
            elif self.master.projectiles[self.round][1] == 2:
                self.master.fullMap.paste(self.master.impact1, (int(self.x)+180, int(self.y)+180), mask=self.master.impact1.split()[3])
            elif self.master.projectiles[self.round][1] == 3:
                self.master.fullMap.paste(self.master.impact3, (int(self.x)+150, int(self.y)+150), mask=self.master.impact3.split()[3])

            self.master.root.after(500, self.master.recon(int(self.x), int(self.y), random.randint(0, 180)))



class gameC:

    def __init__(self):
    
        #starting variables
        self.impact1 = 0
        self.screen = 1
        self.prevScr = 0
        self.directivesLn = -1
        self.mapOffset = (960, 650)
        self.azRad = 0
        self.elRad = 0
        self.loaded = 0
        self.select = 1
        self.projectiles = (("AP", 1, "grey"), ("HE", 2, "RED"), ("WP", 3, "white"), ("CH", 3, "green"))
        #making screen
        self.root = tk.Tk() #root window i think
        self.root.title("iron nest ripoff")#title
        self.root.geometry("1920x1080+0+0")
        #making canvas
        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg="black")
        self.canvas.pack()

        #images
        self.fullMap = Image.open("greyscalemap.png")
        self.pixel = tk.PhotoImage(width=1, height=1)#invisible pixel for button sizing i guess
            #map displays
        self.blankMap = Image.new("RGBA", (1920, 1080), color=(0,0,0,0))
        self.brightness = ImageEnhance.Brightness(self.fullMap)
        self.blankMap.paste(self.brightness.enhance(0.2), (0,0))


        self.map_1 = ImageTk.PhotoImage(self.blankMap)
            #craters
        self.impact1 = Image.open("smallishimpact.png")
        self.impact2 = Image.open("smallimpact2.png")
        self.impact3 = Image.open("smoke.png")

        #buttons for screen change
        self.mapB1 = tk.Button(self.root, text="Map", width=300, height=140, image=self.pixel,compound="left", command=self.bone, font=("arial", 40, "bold"))
        self.mapB2 = tk.Button(self.root, text="Directives", width=300, height=140, image=self.pixel,compound="left", command=self.btwo, font=("arial", 40, "bold"))
        self.mapB3 = tk.Button(self.root, text="Breach", width=300, height=140, image=self.pixel,compound="left", command=self.bthree, font=("arial", 40, "bold"))
        #other ones
        self.directivesBox = tk.Text(self.root, width=70, height=50)
        self.shootB = tk.Button(self.root, text="Fire", width=300, height=140, image=self.pixel,compound="left", command=self.shoot, bg="red", font=("arial", 40, "bold"))
        self.ramB = tk.Button(self.root, text="Ram", width=300, height=140, image=self.pixel,compound="left", command=self.ram, bg="red", font=("arial", 40, "bold"))


        #cranks for elevation / azimuth
        self.knobE = ImageKnob(self.root, image="handle.png", text_color="white",end=600, text="Elevation ", bg="grey38", start_angle=0,scale_width=70, end_angle=-7200, scroll_steps=1, radius=200, command=lambda: updateDial(self.knobE, f"Elevation: {self.knobE.get()/10}°"))
        self.knobA = ImageKnob(self.root, image="handle.png", text_color="white",start=-600, end=600, text="Azimuth ", bg="grey38", start_angle=18000,scale_width=70, end_angle=-18000, scroll_steps=1, radius=200, command=lambda: updateDial(self.knobA, f"Azimuth: {self.knobA.get()/10}°"))
        self.knobA.set(0)
        #ammo selector
        self.knobG = ImageKnob(self.root, image="handle.png", text_color="white",start=0, end=3, text=self.projectiles[self.select][0], bg="black", start_angle=18,scale_width=70, end_angle=-180, scroll_steps=1, radius=200)



        #summoning screen change buttons at start on canvas
        self.canvas.create_window(550, 80, window=self.mapB1)
        self.canvas.create_window(960, 80, window=self.mapB2)
        self.canvas.create_window(1370, 80, window=self.mapB3)

        #cranks and shoot
        self.crankE = self.canvas.create_window(1800, 600, window=self.knobE)
        self.crankA = self.canvas.create_window(1700, 800, window=self.knobA)
        self.shootBC =self.canvas.create_window(1300, 900, window=self.shootB)
        self.ramBC = self.canvas.create_window(800, 900, window=self.ramB)
        self.crankG = self.canvas.create_window(900, 600, window=self.knobG)

        #directives
        self.directivesBoxWindow = self.canvas.create_window(450, 550, window=self.directivesBox) #reading directives text file
        with open("directives.txt", "r", encoding="utf-8") as file:
            self.lines = file.readlines()

        self.nextMission()

        self.recon(630, 600, 1)#shows gun position
        #loops or sum
        self.menuloop()#starts menu loop
        self.root.mainloop()#starts entire everything I think

    def mouseX(self):
        # 1. Get absolute screen coordinates
        screen_x = self.root.winfo_pointerx()
        
        
        # 2. Subtract window position to get coordinates relative to the window
        win_x = screen_x - self.root.winfo_rootx()
        
        return(win_x)
    
    def mouseY(self):
        screen_y = self.root.winfo_pointery()
        win_y = screen_y - self.root.winfo_rooty()
        return(win_y)


    def nextMission(self):#plays next set of directives I think(haven't properly tested this yet)
        self.directivesLn +=1
        self.directivesBox.insert("end", "---------------------------------------------------------------------\n")
        while(self.lines[self.directivesLn].strip()):
            self.directivesBox.insert("end", self.lines[self.directivesLn])
            self.directivesLn += 1

    def menuloop(self):
        self.canvas.delete("gun")
        self.canvas.delete("shell")
        self.canvas.delete("indicator")
        if self.loaded >= 1:
            self.shootB.config(bg="red")
        else:
            self.shootB.config(bg="grey", fg="black")
        if self.screen ==1:
            if not self.prevScr == 1: #page 1 init
                self.mapdisplay = self.canvas.create_image(self.mapOffset[0],self.mapOffset[1],image=self.map_1, tags="map")#map display
                #change buttons to show what screen is up
                self.mapB1.config(bg="green", fg="black")
                self.mapB2.config(bg="grey", fg="black")
                self.mapB3.config(bg="grey", fg="black")

                self.canvas.itemconfigure(self.directivesBoxWindow, state="hidden")#change what windows are visible
                self.canvas.itemconfigure(self.crankE, state="hidden")
                self.canvas.itemconfigure(self.crankA, state="hidden")
                self.canvas.itemconfigure(self.crankG, state="hidden")
                self.canvas.itemconfigure(self.shootBC, state="hidden")
                self.canvas.itemconfigure(self.ramBC, state="hidden")

            mx, my = self.mouseX(), self.mouseY()
            self.canvas.create_line(830, 900, mx,my, tags="indicator", fill="white")
            self.canvas.create_text(mx, my-30, text=f"{round(m.degrees(m.atan2(my-900, mx-830)+m.pi/2)*10)/10}°, {round(m.dist((mx, my), (830, 900)))}m", tags="indicator", fill="white")
        elif self.screen == 2:
            if not self.prevScr == 2:#page 2 init
                self.canvas.delete("map")
                #change buttons to show what screen is up
                self.mapB1.config(bg="grey", fg="black")
                self.mapB2.config(bg="green", fg="black")
                self.mapB3.config(bg="grey", fg="black")

                self.canvas.itemconfigure(self.directivesBoxWindow, state="normal")#change what windows are visible
                self.canvas.itemconfigure(self.crankE, state="hidden")
                self.canvas.itemconfigure(self.crankA, state="hidden")
                self.canvas.itemconfigure(self.crankG, state="hidden")
                self.canvas.itemconfigure(self.shootBC, state="hidden")
                self.canvas.itemconfigure(self.ramBC, state="hidden")

        else:
            if not self.prevScr == 3:#page 3 init
                self.canvas.delete("map")
                #change buttons to show what screen is up
                self.mapB1.config(bg="grey", fg="black")
                self.mapB2.config(bg="grey", fg="black")
                self.mapB3.config(bg="green", fg="black")

                self.canvas.itemconfigure(self.directivesBoxWindow, state="hidden")#change what windows are visible
                self.canvas.itemconfigure(self.crankE, state="normal")
                self.canvas.itemconfigure(self.crankA, state="normal")
                self.canvas.itemconfigure(self.crankG, state="normal")
                self.canvas.itemconfigure(self.shootBC, state="normal")
                self.canvas.itemconfigure(self.ramBC, state="normal")

            #draw gun stuff
            gunPoints = ((-400,80),(-400,-80),(200,-80),(600,-50),(600,50),(200,80))#barrel points relative to turning point
            self.canvas.create_arc((1300, 000, 1900, 600,), fill="grey30", start=(self.knobE.get()/10)+220, extent=90, tags="gun")#trunion ring gear
            self.canvas.create_polygon(rotatePolygon((self.knobE.get()/-10),gunPoints, 1600, 300), fill="grey", tags="gun")#rotating barrel/chamber
            self.canvas.create_polygon(((0,800),(0,1000),(1920,1000),(1920,800),(1920,500),(1700,500),(1500,800)), fill="grey38", tags="gun")#elevation mechanism mount
            self.canvas.create_oval(1560,260, 1640,340, fill="grey30", tags="gun", outline="grey30")#circle
            #shell
            if not self.loaded:
                self.canvas.create_rectangle(800, 250, 1100, 350, fill=self.projectiles[self.select][2], tags="shell")
                updateDial(self.knobG, self.projectiles[self.select][0])


            if self.knobE:
                self.elRad = m.radians(self.knobE.get()/10)
            if self.knobA:
                self.azRad = m.radians(self.knobA.get()/10)
            if self.knobG:
                self.select = self.knobG.get()
        


        self.prevScr = self.screen
        self.root.after(10, self.menuloop)

    def recon(self, ix, iy, dir):
        section = self.fullMap.convert("RGBA")
        section = section.crop((ix,iy,300+ix,300+iy))#section for image

        poly = Image.new("RGBA", (300, 300), color=(0,0,0,0))#mask for image
        poly2 = ImageDraw.Draw(poly)

        points = ((-50,100),(50,100),(50,-100),(-50,-100))#drawing on mask for image
        pointsR = rotatePolygon(dir, points, 200,200)
        poly2.polygon(pointsR, fill="orange")# i don't remembr why its orange but it works i guess

        mask = poly.split()[3]#mask alpha
        self.blankMap.paste(section, (ix,iy), mask=mask)#mask for image applying masked section
        self.map_1 = ImageTk.PhotoImage(self.blankMap)
        self.mapdisplay = self.canvas.create_image(self.mapOffset[0],self.mapOffset[1],image=self.map_1, tags="map")#updating map display

    def shoot(self):
        if self.loaded >= 1:
            projectile(self, self.loaded-10) #un offsets and shoots projectile
            self.loaded = 0
    def ram(self):
        if not self.loaded:
            self.loaded = self.select+10#offsets it to not be 0 for statements

    #screen tab buttons
    def bone(self):
        self.screen = 1
    def btwo(self):
        self.screen = 2
    def bthree(self):
        self.screen = 3

    



game = gameC()#makes game
















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