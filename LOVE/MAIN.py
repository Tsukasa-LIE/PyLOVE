import random
from tkinter import *
from math import sin, cos, pi, log

CANVS_WIDTH = 640
CANVS_HEIGHT = 480
CANVS_CENTER_X = CANVS_WIDTH / 2
CANVS_CENTER_Y = CANVS_HEIGHT /2
IMAGE_ENLARGE = 8

def heart_function(t):
    x = 15 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(t) - cos(4 * t))
    x *= IMAGE_ENLARGE
    y *= IMAGE_ENLARGE
    x += CANVS_CENTER_X
    y += CANVS_CENTER_Y
    return int(x), int(y)
def scatter_inside(x, y, beta=0.15):
    ratiox = - beta * log(random.random())
    ratioy = - beta * log(random.random())
    dx = ratiox * (x - CANVS_CENTER_X)
    dy = ratioy * (y - CANVS_CENTER_Y)
    return x -dx, y-dy
def shrink(x, y, ratio):
    force =  1 / (((x - CANVS_CENTER_X) ** 2 + (y - CANVS_CENTER_Y) ** 2) ** 0)
    dx = ratio * force * (x - CANVS_CENTER_X)
    dy = ratio * force * (y - CANVS_CENTER_Y)
    return x - dx, y - dy

class Heart:
    def __init__(self):
        self.points = set()
        self.build(2000)
    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x,y = heart_function(t)
            self._points.add((int(x),int(y)))
        for xx, yy in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(xx, yy, 0.05)
                self._extra_points.add((x,y))
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y)
            self._inside.add((int(x), int(y)))
    def calc_position(self, x, y, ratio):
        force = 1 / (((x - CANVS_CENTER_X) ** (y - CANVS_CENTER_Y) ** 2))
        dx = ratio * force * (x - CANVS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy
    def calc(self, frame):
        calc_position = self.calc_position
        ratio = 20 * sin(frame / 10 * pi)
        all_points = []
        for x, y in self._points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self.extra_points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self._inside:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        self.all_points[frame] = all_points
    def render(self, canvas, frame):
         for x, y, size in self.all_points[frame % 20]:
            canvas.create_rectangle(x, y, x + size, y + size, width = 0 , fill = "#ff7171" )
def draw(root: Tk, canvas: Canvas , heart: Heart, frame = 0):
    canvas.deleta('all')
    heart.render(canvas, frame)
    root.after(30, draw, root, canvas, heart, frame ++ 1)
if __name__ == "__mian__":
    root = Tk()
    canvas = Canvas(root ,bg = "black", height = CANVS_HEIGHT, width = CANVS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()