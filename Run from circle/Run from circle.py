from tkinter import *

def move(vector):
    if (vector == UPKEY):
        cnv.move(player, 0, -playerSpeed)
    elif (vector == DOWNKEY):
        cnv.move(player, 0, playerSpeed)
    elif (vector == LEFTKEY):
        cnv.move(player, -playerSpeed, 0)
    elif (vector == RIGHTKEY):
        cnv.move(player, playerSpeed, 0)

def evilMove():
    global evilAfter, vectorX, vectorY

    cnv.move(evil, vectorX, vectorY)

    x = cnv.coords(evil)[0]
    y = cnv.coords(evil)[1]

    if (x > WIDTH - 32 or x < 32):
        vectorX = -vectorX
    if (y > HEIGHT - 32 or y < 32):
        vectorY = -vectorY

    xP = cnv.coords(player)[0]
    yP = cnv.coords(player)[1]

    distance = (abs(x - xP) ** 2 + abs(y - yP) ** 2) ** 0.5

    if (distance < 64):
        root.after_cancel(evilAfter)
    else:
        evilAfter = root.after(30, evilMove)

WIDTH = 640
HEIGHT = 480

root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")

cnv = Canvas(root, width=WIDTH, height=HEIGHT)
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

back = PhotoImage(file="background.png")
cnv.create_image(WIDTH // 2, HEIGHT // 2, image=back)
evilCircle = PhotoImage(file="circle.png")
playerSquare = PhotoImage(file="square.png")

vectorX = 3
vectorY = 12

playerSpeed = 5

evil = cnv.create_image(32, 32, image=evilCircle)
player = cnv.create_image(WIDTH // 2, HEIGHT // 2, image=playerSquare)

UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

cnv.bind("<Up>", lambda e, x = UPKEY: move(x))
cnv.bind("<Down>", lambda e, x = DOWNKEY: move(x))
cnv.bind("<Left>", lambda e, x = LEFTKEY: move(x))
cnv.bind("<Right>", lambda e, x = RIGHTKEY: move(x))

evilAfter = root.after(17, evilMove)

root.mainloop()
