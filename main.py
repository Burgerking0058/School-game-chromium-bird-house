import tkinter as tk
import math as m
from PIL import Image, ImageTk
global screen
screen = 1
global prevScr
prevScr = 0
global directivesLn
directivesLn = -1
global lines


def labelledBox(x, y, w, h, fill, stroke, text, tag):
    canvas.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, fill=fill, tags=tag)
    canvas.create_text(x,y, fill=stroke, text=text, tags=tag)

def nextMission():
    global directivesLn
    global lines
    directivesLn +=1
    while(lines[directivesLn].strip()):
        directivesBox.insert("end", lines[directivesLn])
        print(lines[directivesLn])
        directivesLn += 1


def menuloop():
    global prevScr
    if screen ==1:
        if not prevScr == 1: #page 1 init
            

            mapdisplay = canvas.create_image(960,570,image=map_1, tags="map")#map display
            #change buttons to show what screen is up
            mapB1.config(bg="green", fg="black")
            mapB2.config(bg="grey", fg="black")
            mapB3.config(bg="grey", fg="black")

            canvas.itemconfigure(directivesBoxWindow, state="hidden")

    elif screen == 2:
        if not prevScr == 2:#page 2 init
            canvas.delete("map")
            #change buttons to show what screen is up
            mapB1.config(bg="grey", fg="black")
            mapB2.config(bg="green", fg="black")
            mapB3.config(bg="grey", fg="black")

            canvas.itemconfigure(directivesBoxWindow, state="normal")
            
    else:
        if not prevScr == 3:#page 3 init
            #change buttons to show what screen is up
            mapB1.config(bg="grey", fg="black")
            mapB2.config(bg="grey", fg="black")
            mapB3.config(bg="green", fg="black")

            canvas.itemconfigure(directivesBoxWindow, state="hidden")


    prevScr = screen
    root.after(10, menuloop)





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


#images
pilImage = Image.open("Map1.png")
map_1 = ImageTk.PhotoImage(pilImage)

pixel = tk.PhotoImage(width=1, height=1)#invisible pixel for button sizing i guess

#buttons for screen change
mapB1 = tk.Button(root, text="Map", width=300, height=140, image=pixel,compound="left", command=bone)
mapB2 = tk.Button(root, text="Directives", width=300, height=140, image=pixel,compound="left", command=btwo)
mapB3 = tk.Button(root, text="Breach", width=300, height=140, image=pixel,compound="left", command=bthree)
directivesBox = tk.Text(root, width=70, height=50)


#summoning screen change buttons at start
canvas.create_window(550, 80, window=mapB1)
canvas.create_window(960, 80, window=mapB2)
canvas.create_window(1370, 80, window=mapB3)
#directives
directivesBoxWindow = canvas.create_window(450, 550, window=directivesBox)




with open("directives.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

nextMission()


#loops or sum
menuloop()
root.mainloop()
