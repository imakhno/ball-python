from tkinter import *
import random
import time

screen = Tk()
screen.title("Game")
screen.resizable(False, False)
screen.wm_attributes("-topmost", 1)
canvas = Canvas(screen, width=500, height=400)
canvas.pack()
screen.update()


# screen.attributes('-fullscreen', True)
# canvas.pack(fill=BOTH, expand=True)


class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10,
                                     25, 25,
                                     fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 200, text='Вы проиграли!', font=('Courier', 30), fill='red')

        if self.hit_paddle(pos):
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3


# класс для создания платформы
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0,
                                          100, 10,
                                          fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, event):
        pos = self.canvas.coords(self.id)
        if pos[0] > 0:
            self.x = -2

    def turn_right(self, event):
        pos = self.canvas.coords(self.id)
        if pos[2] < self.canvas_width:
            self.x = 2


class Score:
    # конструктор
    def __init__(self, canvas, color):
        # в самом начале счёт равен нулю
        self.score = 0
        # будем использовать наш холст
        self.canvas = canvas
        # создаём надпись, которая показывает текущий счёт,
        # делаем его нужно цвета и запоминаем внутреннее имя этой надписи
        self.id = canvas.create_text(
            450, 10,
            text=self.score,
            font=('Courier', 15),
            fill=color)

    # обрабатываем касание платформы
    def hit(self):
        # увеличиваем счёт на единицу
        self.score += 1
        # пишем новое значение счёта
        self.canvas.itemconfig(self.id, text=self.score)


score = Score(canvas, 'green')
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, score, 'red')

while True:
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
    else:
        time.sleep(2)
        break
    screen.update_idletasks()
    screen.update()
    time.sleep(0.01)
