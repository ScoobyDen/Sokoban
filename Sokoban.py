from tkinter import *
from time import sleep
from winsound import Beep

def goCheat():
    pass

def getNumber(x, y):
    pass

def movePlayerTo(x, y, count):
    pass

def movePlayerBoxTo(x, y, count, numberBox):
    pass

def getBox(x, y):
    pass

#повертаємо строку у вигляді ММ:СС
def getMinSec(s):
    intMin = s // 60                                #знаходимо хвилини
    intSec = s % 60                                 #знаходимо залишок секунд
    textSecond = str(intSec)
    if (intMin > 59):
        intMin %= 60
    #додаємо 0 якщо секунд менше 10
    if (intSec < 10):
        textSecond = "0" + textSecond
    if (intMin == 0):
        return f"{textSecond} сек."
    else:
        textMin = str(intMin)
        if (intMin < 10):
            textMin = "0" + textMin
        return f"{textMin} хв. {textSecond} сек."

#оновлюємо полоску з текстом уверху
def updateText():
    global textTime, second, timeRun
    second += 1                                                                                         #збільшуємо кількісь секунд з -1
    cnv.delete(textTime)                                                                                #видаляємо минулий текст, якщо цього не зробити то текст буде накладуватися один на одного
    txt = f"Рівень: {level}   Пройшло часу: {getMinSec(second)}"                                        #формуємо строку виводу
    textTime = cnv.create_text(10, 10, fill="#FFCAAB", anchor="nw", text=txt, font="Verdana, 15")       #створюємо змінну для таймеру, вона потрібна щоб програма мала ссилку на таймер, коли нам потрібно буде припинити відлік
    timeRun = root.after(1000, updateText)                                                              #вішаємо timeRun на виклик updateText() кожну секунду (1000 мс)

#створення об'єктів в Canvas формуємо зображення позицій
def createLevel():
    print("Метод createLevel()")
    global player, boxes, finish
    player = []
    boxes = []
    finish = []
    #малюємо нижній слой: стіни та місця для сбору
    for i in range(len(dataLevel)):
        for j in range(len(dataLevel[i])):
            if (dataLevel[i][j] == 1):
                cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE, SQUARE_SIZE // 2  + i * SQUARE_SIZE, image=img[0])
            elif (dataLevel[i][j] == 3):
                dataLevel[i][j] = 0
                finish.append([i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE, SQUARE_SIZE // 2  + i * SQUARE_SIZE, image=img[2]), False])
                #Данні списку finish[a, b, c, d]: 
                # a - координата по х відносно матиматичної моделі 20х10
                # b - координата по y -""-
                # c - об'єкт image на Canvas (зелена точка)
                # d - ознака True - є на цій клітині, False - немає

    #малюємо верхній слой
    for i in range(len(dataLevel)):
        for j in range(len(dataLevel[i])):
            if (dataLevel[i][j] == 2):
                dataLevel[i][j] = 0
                boxes.append([i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE, SQUARE_SIZE // 2  + i * SQUARE_SIZE, image=img[1])])
                #Данні списку boxes[a, b, c]: 
                # a - координата по х відносно матиматичної моделі 20х10
                # b - координата по y -""-
                # c - об'єкт image на Canvas (ящик)
            elif (dataLevel[i][j] == 4):
                dataLevel[i][j] = 0
                player = [i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE, SQUARE_SIZE // 2  + i * SQUARE_SIZE, image=img[3][1])]
                #Данні списку player[a, b, c]: 
                # a - координата по х відносно матиматичної моделі 20х10
                # b - координата по y -""-
                # c - об'єкт image на Canvas (вантажник)

#замостити зображенням трави всю область вікна
#мєтод треба визивати самим першим, щоб він був у самому нижньому слої
def clear_setGrass():
    print("Метод clear_setGrass()")
    cnv.delete(ALL)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            cnv.create_image(SQUARE_SIZE // 2 + i * SQUARE_SIZE, SQUARE_SIZE // 2 + j * SQUARE_SIZE, image=backGround)

#завантаження данних рівня
def getLevel(lvl):
    global dataLevel
    print("Метод getLevel()")
    dataLevel = []
    tmp = []

    #формуємо індекс до імені файлу, idx буде зберігати 08, 09, 10, 11 в заледності від змінної level
    idx = str(lvl)
    if (lvl < 10):
        idx = f"0{lvl}"
    try:
        f = open(f"levels/level{idx}.dat", "r", encoding="utf-8")
        for i in f.readlines():
            tmp.append(i.replace("\n", ""))
        f.close()
        #перегоняємо в двовимірний список з числами
        for i in range(len(tmp)):
            dataLevel.append([])
            for j in tmp[i]:
                dataLevel[i].append(int(j))
    except:
        print("Не знайдено файлу з данним")
        quit(0)

#зупинка таймеру
def stopTimer():
    global timeRun
    if (timeRun != None):
        root.after_cancel(timeRun)
        timeRun = None

#сброс та перезавантаження рівня
def reset():
    global moving, second, timeRun
    print("Метод reset()")
    moving = False
    second = -1
    stopTimer()
    getLevel(level)
    clear_setGrass()
    createLevel()
    updateText()

def move(v):
    print("Метод move()")

    if (moving):
        return 0
    cnv.delete(player[2])
    player[2] = cnv.create_image(SQUARE_SIZE // 2 + player[1] * SQUARE_SIZE, SQUARE_SIZE // 2 + player[0] * SQUARE_SIZE, image=img[3][v])
    x = player[0]
    y = player[1]
    Beep[625, 10]

    if (v == UPKEY):
        check = getNumber(x - 1, y)
        if (check == 0):
            movePlayerTo(0, -8, 8)
            player[0] -= 1
        elif (check == 2):
            nextCheck = getNumber(x - 2, y)
            if (nextCheck == 0):
                numberBox = getBox(x - 1, y)
                movePlayerBoxTo(0, -8, 8, numberBox)
                player[0] -= 1
                boxes[numberBox][0] -= 1
    elif (v == DOWNKEY):
        check = getNumber(x + 1, y)
        if (check == 0):
            movePlayerTo(0, 8, 8)
            player[0] += 1
        elif (check == 2):
            nextCheck = getNumber(x + 2, y)
            if (nextCheck == 0):
                numberBox = getBox(x + 1, y)
                movePlayerBoxTo(0, 8, 8, numberBox)
                player[0] += 1
                boxes[numberBox][0] += 1
    elif (v == LEFTKEY):
        check = getNumber(x, y - 1)
        if (check == 0):
            movePlayerTo(-8, 0, 8)
            player[1] -= 1
        elif (check == 2):
            nextCheck = getNumber(x, y - 2)
            if (nextCheck == 0):
                numberBox = getBox(x, y - 1)
                movePlayerBoxTo(-8, 0, 8, numberBox)
                player[0] -= 1
                boxes[numberBox][0] -= 1
    elif (v == RIGHTKEY):
        check = getNumber(x, y + 1)
        if (check == 0):
            movePlayerTo(8, 0, 8)
            player[1] += 1
        elif (check == 2):
            nextCheck = getNumber(x, y + 2)
            if (nextCheck == 0):
                numberBox = getBox(x, y + 1)
                movePlayerBoxTo(8, 0, 8, numberBox)
                player[0] += 1
                boxes[numberBox][0] += 1

#===============================Start programm =========================================
#створюємо вікно
root = Tk()
root.resizable(False, False)
root.title("Sokoban by DF")
#іконка
root.iconbitmap("icon/icon.ico")

#кількість плиток по ширені та висоті
WIDTH = 20
HEIGHT = 10
#розмір однієї плитки
SQUARE_SIZE = 64

POS_X = root.winfo_screenwidth() // 2 - (WIDTH * SQUARE_SIZE) // 2
POS_Y = root.winfo_screenheight() // 2 - (HEIGHT * SQUARE_SIZE) // 2
root.geometry(f"{WIDTH * SQUARE_SIZE + 0}x{HEIGHT * SQUARE_SIZE + 0}+{POS_X}+{POS_Y}")

#константи напрямку руху
UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

#КАНВАС
cnv = Canvas(root, width=WIDTH*SQUARE_SIZE, height=HEIGHT*SQUARE_SIZE, bg="#373737")
#обмежувальна рамка
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

#призначення клавіш
cnv.bind("<Up>", lambda e, x=UPKEY: move(x))
cnv.bind("<Down>", lambda e, x=DOWNKEY: move(x))
cnv.bind("<Left>", lambda e, x=LEFTKEY: move(x))
cnv.bind("<Right>", lambda e, x=RIGHTKEY: move(x))

#якщо True то move(x) виконуватися не буде
moving = True
#текстура фону
backGround = PhotoImage(file="image/grass.png")

#список для збереження зображень
img = []
img.append(PhotoImage(file="image/wall.png"))
img.append(PhotoImage(file="image/box.png"))
img.append(PhotoImage(file="image/finish.png"))
img.append([])
img[3].append(PhotoImage(file="image/kosoban_up.png"))
img[3].append(PhotoImage(file="image/kosoban_down.png"))
img[3].append(PhotoImage(file="image/kosoban_left.png"))
img[3].append(PhotoImage(file="image/kosoban_right.png"))

#об'єкт (список) гравець
player = None
#ящики (список)
boxes = None
#місця для ящиків (список)
finish = None
#перемога?
win = False

#кнопка відновлення ігрового поля на початкову позицію
btnReset = Button(text="Зкинути поле".upper(), font=("Consolas", "15"), width=20)
btnReset.place(x=10, y=550)
btnReset["command"] = reset

#чіт-кнопка
btnCheat = Button(text="Чіт-код".upper(), font=("Consolas", "15"), width=20)
btnCheat.place(x=10, y=590)
btnCheat["command"] = goCheat

#глобальні об'єкти
#текстова строка яка показує час
textTime = None
#минулий час
second = None
#рівень
level = 5

#данні про ігрове поле, завантажуються з файла
dataLevel = []
#змінна для таймеру, необхідна для зупинки роботи root.after()
timeRun = None
#створюємо рівень
reset()
root.mainloop()