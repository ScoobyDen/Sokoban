from tkinter import *

def go(vector):
    if (vector == UPKEY):
        cnv.move(player, 0, -2)
    elif (vector == DOWNKEY):
        cnv.move(player, 0, 2)
    elif (vector == LEFTKEY):
        cnv.move(player, -2, 0)
    elif (vector == RIGHTKEY):
        cnv.move(player, 2, 0)

#Розміри вікна
WIDTH = 640
HEIGHT = 480

root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")

#створюємо Canvas
cnv = Canvas(root, width=WIDTH, height=HEIGHT)
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

#забраження заднього фону
back = PhotoImage(file="background.png")
cnv.create_image(WIDTH // 2, HEIGHT // 2, image=back)

#зображення круга
evilCircle = PhotoImage(file="circle.png")
evil = cnv.create_image(32, 32, image=evilCircle)

#зображення зеленого кварату
playerSquare = PhotoImage(file="square.png")
player = cnv.create_image(WIDTH // 2, HEIGHT // 2, image=playerSquare)

#закодуємо кнопки для переміщення
UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

cnv.bind("<Up>", lambda e, x = UPKEY: go(x))
cnv.bind("<Down>", lambda e, x = DOWNKEY: go(x))
cnv.bind("<Left>", lambda e, x = LEFTKEY: go(x))
cnv.bind("<Right>", lambda e, x = RIGHTKEY: go(x))

root.mainloop()