from PIL import Image, ImageColor, ImageFilter
import random
from math import *

#<shittycode_mode_on>

_width, _height = 640, 960

width = _width * 2
height = _height * 2

paper = Image.open('paper.png')

image = Image.new('RGB', (width, height))
stub = image.getdata()

def cached(function):
       cache = {}
       def wrapper(*args):
              if args not in cache:
                     cache[args] = function(*args)
              return cache[args]
       return wrapper

@cached
def hsl(h, s, l):          
       return ImageColor.getrgb('hsl(%d,%d%%,%d%%)' % (h, s, l))

area_x, area_y = [], []
y = 0
while y < height:
       y += random.randrange(30, 60)
       area_y.append(y)

x = 0
while x < width:
       x += random.randrange(30, 60)
       area_x.append(x)

offset_x = [random.randrange(0, 50) for _ in area_y]
offset_y = [random.randrange(0, 50) for _ in area_x]

def getarea_grid(x, y):
       if True: #random.randint(0, 1) == 0:
              j = 0
              while y > area_y[j]:
                     j += 1
              x_moved = ( x + offset_x[j] ) % width
              i = 0
              while x_moved > area_x[i]:
                     i += 1
              return i + 2 * j
       else:
              i = 0
              while x > area_x[i]:
                     i += 1
              y_moved = ( y + offset_y[i] ) % height
              j = 0
              while y_moved > area_y[j]:
                     j += 1
              return i + 2 * j

area_y = []
y = 0
for _ in xrange(60):
       y += random.randint(50, 70)
       w = random.randint(30, 50) * 1.0
       o = random.randint(0, 30) * 1.0
       a = random.randint(10, 30)
       area_y.append( [int(y + a * sin((x + o)/w)) for x in xrange(width)] )

area_x = []
x = 0
for _ in xrange(60):
       x += random.randint(50, 70)
       w = random.randint(30, 50) * 1.0
       o = random.randint(0, 30) * 1.0
       a = random.randint(10, 30)
       area_x.append( [int(x + a * sin((y + o)/w)) for y in xrange(height)] )


def getarea(x, y):
       j = 0
       while area_y[j][x] < y:
              j += 1
       i = 0
       while area_x[i][y] < x:
              i += 1
       return i + 2 * j

palette = map(ImageColor.getrgb, ['#229396', '#8BA88F', '#C7C5A8', '#F0DFD0', '#F23C3C'])
def getcolor(x, y):
       #palette = [hsl(0,80,50), hsl(20,80,50), hsl(40,80,50), hsl(60,80,50), hsl(80,80,50)]
       return palette[getarea(x, y) % len(palette)]

#</shittycode_mode_on>

data = [getcolor(i % width, i / width) for i, x in enumerate(stub)]

image.putdata(data)

_image = Image.blend(image.resize((_width, _height), Image.ANTIALIAS), paper.convert('RGB'), 0.3)

_image.save('x.png')
