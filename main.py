import tkinter as tk
import math as m
from PIL import Image, ImageTk
global screen
screen = 1







root = tk.Tk() #root window i think
root.title("iron nest ripoff")#title
root.geometry("1920x1080+0+0")

canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
canvas.pack()


def larrow(self):
    if screen >=2:
        screen -=1
def rarrow(self):
    if screen <=2:
        screen +=1


def kill(self):
    root.destroy()
root.bind("<Escape>", kill)
root.bind("<Left>", larrow)
root.bind("<Right>", rarrow)

pilImage = Image.open("Map1.png")
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(400,400,image=image)








root.mainloop()
