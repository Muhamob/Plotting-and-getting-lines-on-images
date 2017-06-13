from matplotlib import pyplot as plt
# import matplotlib.image as mpimg
import numpy as np
from matplotlib.widgets import Button
import matplotlib.patches as patches
import os
from PIL import Image


f = open('/home/alexandr/Desktop/learning/pythonL/task4sem/data.txt', 'r+')
max_num_of_pic = 4
default_num_of_pic = 10
number_of_pic = 1
imgs = []


def getfiles(list_of_imgs):
    global max_num_of_pic
    i = 0
    for item in os.scandir('/home/alexandr/Desktop/learning/pythonL/task4sem/images'):
        if (i < max_num_of_pic) or (i < default_num_of_pic):
            print(item.name)
            list_of_imgs.append(Image.open('/home/alexandr/Desktop/learning/pythonL/task4sem/images/' + item.name))
            i += 1


getfiles(imgs)


fig = plt.figure()
ax = fig.add_subplot(111)


maxsizeX = max([i.size[0] for i in imgs])
maxsizeY = max([i.size[1] for i in imgs])


plt.xlim([0, imgs[0].size[0]])
plt.ylim([0, imgs[0].size[1]])
ax.imshow(imgs[0])


x = []
y = []
points = []

def get_coords(event):
    global x, y
    if event.inaxes != ax:
        return
    x.append(event.xdata)
    y.append(event.ydata)
    print('get is ok')
    rect = patches.Circle((event.xdata, event.ydata), 1)
    ax.add_patch(rect).set_color('#990066')
    ax.figure.canvas.draw()
    print(x[-1], y[-1])

fig.canvas.mpl_connect('button_press_event', get_coords)


__A, __C = 0, 0
coeficents = []


def draw_line_from_xy_and_aprox(event):
    global __A, __C, x, y, points
    if len(x) < 2:
        return
    A = np.vstack([x, np.ones(len(x))]).T
    __A, __C = np.linalg.lstsq(A, y)[0]
    # aproxLine = patches.Polygon()
    ax.plot([min(x), max(x)], [__C + __A*min(x), __C + __A*max(x)], color='#0066ff')
    fig.canvas.draw()
    print('in y = ax + b : a is ' + str(__A) + ' b is ' + str(__C))
    points = [min(x), __C + __A*min(x), max(x), __C + __A*max(x)]
    x, y = [], []


def clear_points_and_xy(event):
    global x, y
    x, y = [], []
    print('clear is ok')


def save_line(event):
    global __A, __C, x, y, points
    f.write(str(number_of_pic) + ' ' + str(__A)+ ' ' + str(points[0]) + ' ' +
            str(points[1]) + ' ' + str(points[2]) + ' ' + str(points[3]) + '\n')
    print('save is ok')
    x, y = [], []
    points = []
    coeficents.append((__A, __C))


def removelast(event):
    f.seek(0, os.SEEK_END)

    # This code means the following code skips the very last character in the file -
    # i.e. in the case the last line is null we delete the last line
    # and the penultimate one
    pos = f.tell() - 1

    # Read each character in the file one at a time from the penultimate
    # character going backwards, searching for a newline character
    # If we find a new line, exit the search
    while pos > 0 and f.read(1) != "\n":
        pos -= 1
        f.seek(pos, os.SEEK_SET)

    # So long as we're not at the start of the file, delete all the characters ahead of this position
    if pos > 0:
        f.seek(pos, os.SEEK_SET)
        f.truncate()

    if coeficents:
        coeficents.pop()
        print('remove is ok')
    else:
        print('already clear')


def nextimg(event):
    global number_of_pic, max_num_of_pic
    ax.cla()
    if number_of_pic < min(max_num_of_pic, default_num_of_pic):
        ax.set_xlim([0, imgs[number_of_pic].size[0]])
        ax.set_ylim([0, imgs[number_of_pic].size[1]])
        ax.imshow(imgs[number_of_pic])
        fig.canvas.draw()
    else:
        plt.close()
    number_of_pic += 1


ax_draw = plt.axes([0.81, 0.01, 0.1, 0.05])
b_draw = Button(ax_draw, 'Draw')
b_draw.on_clicked(draw_line_from_xy_and_aprox)

ax_clear = plt.axes([0.81-0.105, 0.01, 0.1, 0.05])
b_clear = Button(ax_clear, 'Clear')
b_clear.on_clicked(clear_points_and_xy)

ax_save = plt.axes([0.81-0.21, 0.01, 0.1, 0.05])
b_save = Button(ax_save, 'Save')
b_save.on_clicked(save_line)

ax_removelast = plt.axes([0.81-0.415, 0.01, 0.2, 0.05])
b_removelast = Button(ax_removelast, 'Remove last')
b_removelast.on_clicked(removelast)

ax_nextimg = plt.axes([0.81-0.52, 0.01, 0.1, 0.05])
b_nextimg = Button(ax_nextimg, 'Next')
b_nextimg.on_clicked(nextimg)


plt.show()
f.close()
