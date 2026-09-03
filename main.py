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
mapOffset = (960, 575)





def labelledBox(x, y, w, h, fill, stroke, text, tag):
    canvas.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, fill=fill, tags=tag)
    canvas.create_text(x,y, fill=stroke, text=text, tags=tag)

def nextMission():#plays next set of directives I think(haven't properly tested this yet)
    global directivesLn
    global lines
    directivesLn +=1
    directivesBox.insert("end", "---------------------------------------------------------------------\n")
    while(lines[directivesLn].strip()):
        time.sleep(2)
        directivesBox.insert("end", lines[directivesLn])
        directivesLn += 1



def menuloop():
    global prevScr
    canvas.delete("gun")
    if screen ==1:
        if not prevScr == 1: #page 1 init
            

            mapdisplay = canvas.create_image(mapOffset[0],mapOffset[1],image=map_1, tags="map")#map display
            #change buttons to show what screen is up
            mapB1.config(bg="green", fg="black")
            mapB2.config(bg="grey", fg="black")
            mapB3.config(bg="grey", fg="black")

            canvas.itemconfigure(directivesBoxWindow, state="hidden")#change what windows are visible
            canvas.itemconfigure(crankE, state="hidden")
            canvas.itemconfigure(crankA, state="hidden")

    elif screen == 2:
        if not prevScr == 2:#page 2 init
            canvas.delete("map")
            #change buttons to show what screen is up
            mapB1.config(bg="grey", fg="black")
            mapB2.config(bg="green", fg="black")
            mapB3.config(bg="grey", fg="black")

            canvas.itemconfigure(directivesBoxWindow, state="normal")#change what windows are visible
            canvas.itemconfigure(crankE, state="hidden")
            canvas.itemconfigure(crankA, state="hidden")


    else:
        if not prevScr == 3:#page 3 init
            canvas.delete("map")
            #change buttons to show what screen is up
            mapB1.config(bg="grey", fg="black")
            mapB2.config(bg="grey", fg="black")
            mapB3.config(bg="green", fg="black")

            canvas.itemconfigure(directivesBoxWindow, state="hidden")#change what windows are visible
            canvas.itemconfigure(crankE, state="normal")
            canvas.itemconfigure(crankA, state="normal")

        #draw gun stuff
        gunPoints = ((-400,80),(-400,-80),(200,-80),(600,-50),(600,50),(200,80))#barrel points relative to turning point
        canvas.create_arc((1300, 000, 1900, 600,), fill="grey30", start=(knobE.get()/10)+220, extent=90, tags="gun")#trunion ring gear
        canvas.create_polygon(rotatePolygon((knobE.get()/-10),gunPoints, 1600, 300), fill="grey", tags="gun")#rotating barrel/chamber
        canvas.create_polygon(((0,800),(0,1000),(1920,1000),(1920,800),(1920,500),(1700,500),(1500,800)), fill="grey38", tags="gun")#elevation mechanism mount
        canvas.create_oval(1560,260, 1640,340, fill="grey30", tags="gun", outline="grey30")#circle
    prevScr = screen
    root.after(10, menuloop)

def rotatePolygon(angleDeg, points, offx, offy):#func to rotate a liste of points for drawing stuff at an angle
    points2 = [list(point) for point in points]
    dirRad = m.radians(angleDeg)
    cos = m.cos(dirRad)
    sin = m.sin(dirRad)
    for i in range(len(points2)):
        points2[i][0], points2[i][1] = int(points2[i][0]*cos - points2[i][1]*sin+offx), int(points2[i][0]*sin + points2[i][1]*cos+offy)
        
    return(points2)


def recon(ix, iy, dir):

    global map_1

    section = fullMap.convert("RGBA")
    section = section.crop((ix,iy,300+ix,300+iy))

    poly = Image.new("RGBA", (300, 300), color=(0,0,0,0))
    poly2 = ImageDraw.Draw(poly)

    points = ((-50,100),(50,100),(50,-100),(-50,-100))
    pointsR = rotatePolygon(dir, points, 200,200)
    poly2.polygon(pointsR, fill="orange")

    mask = poly.split()[3]
    #mask = mask.resize(section.size)
    blankMap.paste(section, (ix,iy), mask=mask)
    #blankMap.paste(mask, (ix,iy) )
    map_1 = ImageTk.PhotoImage(blankMap)
    mapdisplay = canvas.create_image(mapOffset[0],mapOffset[1],image=map_1, tags="map")#map display


def testClick(event):
    print(f"{event.x}, {event.y}")
    if screen == 1:
        recon(event.x, event.y, random.randint(-90,90))




root = tk.Tk() #root window i think
root.title("iron nest ripoff")#title
root.geometry("1920x1080+0+0")

canvas = tk.Canvas(root, width=1920, height=1080, bg="black")
canvas.pack()

#screen tab button
def bone():
    global screen
    screen = 1
def btwo():
    global screen
    screen = 2
    nextMission()
    
def bthree():
    global screen
    screen = 3

#arrows to switch tabs
def larrow(self):
    global screen
    if screen >=2:
        screen -=1
def rarrow(self):
    global screen
    if screen <=2:
        screen +=1

#close the program with esc
def kill(self):
    root.destroy()
#keybinds
root.bind("<Escape>", kill)
root.bind("<Left>", larrow)
root.bind("<Right>", rarrow)

canvas.bind("<Button-1>", testClick)

def updateDial(dial, text):
    dial.configure(text=f"{text}{dial.get()/10}°")



#images
fullMap = Image.open("Map1.png")
#map_1 = ImageTk.PhotoImage(fullMap)


pixel = tk.PhotoImage(width=1, height=1)#invisible pixel for button sizing i guess

#map displays
blankMap = Image.new("RGBA", (1920, 1080), color=(0,0,0,0))

map_1 = ImageTk.PhotoImage(blankMap)

#buttons for screen change
mapB1 = tk.Button(root, text="Map", width=300, height=140, image=pixel,compound="left", command=bone)
mapB2 = tk.Button(root, text="Directives", width=300, height=140, image=pixel,compound="left", command=btwo)
mapB3 = tk.Button(root, text="Breach", width=300, height=140, image=pixel,compound="left", command=bthree)
directivesBox = tk.Text(root, width=70, height=50)

knobE = ImageKnob(root, image="handle.png", text_color="white",end=600, text="Elevation ", bg="grey38", start_angle=0,scale_width=70, end_angle=-7200, scroll_steps=1, radius=200, command=lambda: updateDial(knobE, "Elevation: "))
knobA = ImageKnob(root, image="handle.png", text_color="white",start=-600, end=600, text="Azimuth ", bg="grey38", start_angle=18000,scale_width=70, end_angle=-18000, scroll_steps=1, radius=200, command=lambda: updateDial(knobA, "Azimuth: "))
knobA.set(0)

#summoning screen change buttons at start
canvas.create_window(550, 80, window=mapB1)
canvas.create_window(960, 80, window=mapB2)
canvas.create_window(1370, 80, window=mapB3)

#cranks
crankE = canvas.create_window(1800, 600, window=knobE)
crankA = canvas.create_window(1700, 800, window=knobA)
#directives
directivesBoxWindow = canvas.create_window(450, 550, window=directivesBox)




with open("directives.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

nextMission()


#loops or sum
menuloop()
root.mainloop()
