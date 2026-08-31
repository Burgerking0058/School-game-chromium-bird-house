import tkinter as tk
import math as m
from PIL import Image, ImageTk
global screen
screen = 1
global prevScr
prevScr = 0



def menuloop():
    global prevScr
    if screen ==1:
        if not prevScr == 1: #page 1 init
            print("init1")
            

            mapdisplay = canvas.create_image(960,570,image=map_1, tags="map")#map display

            canvas.delete("buttons")
            canvas.create_rectangle(400, 10, 700, 150, fill="White", tags="buttons") #left
            canvas.create_rectangle(1130, 10, 810, 140, fill="White", tags="buttons") #mid
            canvas.create_rectangle(1520, 10, 1220, 140, fill="White", tags="buttons") #right
            


    elif screen == 2:
        if not prevScr == 2:#page 2 init
            canvas.delete("map")
            print("2")

            canvas.delete("buttons")
            canvas.create_rectangle(400, 10, 700, 140, fill="White", tags="buttons") #left
            canvas.create_rectangle(1130, 10, 810, 150, fill="White", tags="buttons") #mid
            canvas.create_rectangle(1520, 10, 1220, 140, fill="White", tags="buttons") #right

    else:
        if not prevScr == 2:#page 3 init
            print("3")

            canvas.delete("buttons")
            canvas.create_rectangle(400, 10, 700, 140, fill="White", tags="buttons") #left
            canvas.create_rectangle(1130, 10, 810, 140, fill="White", tags="buttons") #mid
            canvas.create_rectangle(1520, 10, 1220, 150, fill="White", tags="buttons") #right

    prevScr = screen
    root.after(10, menuloop)





root = tk.Tk() #root window i think
root.title("iron nest ripoff")#title
root.geometry("1920x1080+0+0")

canvas = tk.Canvas(root, width=1920, height=1080, bg="black")
canvas.pack()


def larrow(self):
    global screen
    if screen >=2:
        screen -=1
def rarrow(self):
    global screen
    if screen <=2:
        screen +=1


def kill(self):
    root.destroy()
root.bind("<Escape>", kill)
root.bind("<Left>", larrow)
root.bind("<Right>", rarrow)


#images
pilImage = Image.open("Map1.png")
map_1 = ImageTk.PhotoImage(pilImage)








menuloop()
root.mainloop()
