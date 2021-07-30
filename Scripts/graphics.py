from PIL import Image
from os import listdir
from os.path import isfile, join
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

# player character is 6 pixels high by 4 pixels wide
# bottom left corner is located at (30, 17)

def frame(pos, dir, images):

    (bg, player, sb, overlay) = images

    frame = bg.crop((pos[0]-30, pos[1]-17, pos[0]+34, pos[1]+15)).convert('RGB')
    w, h = player.size
    if dir=="left" or dir =="lu" or dir =="ld":
        pp = player.crop((0,0,int(w/4),h-1))
    elif dir=="right" or dir=="ru" or dir=="rd":
        pp = player.crop((int(w/2),0,int(3*w/4),h-1))
    elif dir=="up":
        pp = player.crop((int(3*w/4),0,w-1,h-1))
    else:
        pp = player.crop((int(w/4),0,int(w/2)-1,h-1))
    frame.paste(pp.convert('RGB'), (30,17), pp.convert('RGBA'))

    print(pos)
    print(sb.size)
    if not sb.convert('RGB').getpixel((pos[0], pos[1])) == (0, 0, 0):
        frame.paste(overlay.convert('RGB'), (0,0), overlay.convert('RGBA'))

    return frame.convert('RGB')

def checkvalidmove(direction, pos, sublevel):
    validmoves = ['left','right','up','down','lu','ru','ld','rd']
    newpos = pos[:]
    if not direction in validmoves:
        return False
    else:
        if direction == 'left':
            newpos[0] = pos[0] -1
        elif direction == 'right':
            newpos[0] = pos[0] +1
        elif direction == 'up':
            newpos[1] = pos[1] -1
        elif direction == 'down':
            newpos[1] = pos[1] +1
        elif direction == 'lu':
            newpos = [pos[0] -1, pos[1] - 1]
        elif direction == 'ru':
            newpos = [pos[0] +1, pos[1] - 1]
        elif direction == 'ld':
            newpos = [pos[0] -1, pos[1] + 1]
        elif direction == 'rd':
            newpos = [pos[0] +1, pos[1] + 1]
        
        if sublevel.convert('RGB').getpixel((newpos[0], newpos[1])) == (255,0,0):
            return False
        else:
            return newpos

def displaycutscene(name, matrix):
    filepath = '../Assets/Cutscenes/'+name
    images = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    images.sort()
    for image in images:
        frame = Image.open(filepath + '/' + image)
        matrix.Clear()
        matrix.SetImage(frame)
        #time.sleep(0.5)
    return