from PIL import Image

# player character is 6 pixels high by 4 pixels wide
# bottom left corner is located at (30, 17)

def frame(pos, dir, images):

    (bg, sb, player, overlay) = images

    frame = bg.crop((pos[0]-30, pos[1]-17, pos[0]+34, pos[1]+15))
    if dir=="left" or dir =="lu" or dir =="ld":
        pp = player.crop((0,0,3,5))
    elif dir=="right" or dir=="ru" or dir=="rd":
        pp = player.crop((8,0,11,5))
    elif dir=="up":
        pp = player.crop((13,0,15,5))
    else:
        pp = player.crop((4,0,7,5))
    frame.paste(pp, (30,17), pp.convert('RGBA'))
    print(pos)
    if not sb.getpixel(pos) == (0, 0, 0):
        frame.paste(overlay, (0,0), overlay)

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
        return newpos