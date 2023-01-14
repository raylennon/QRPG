import time
import threading
import sys

import platform

debug = (platform.platform()[0:7]=="Windows")
if debug:
    from cv2_debugscreen import TestScreen
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

from PIL import Image

import flask
from flask import Flask, render_template, Response, request, redirect, url_for

import createqrcode
import graphics

import os

current_level = "Demo Scene"

# load all of the images into memory for speed purposes?

bg = Image.open('../Assets/Levels/' + current_level + '/background.png')
player = Image.open('../Assets/Misc/Player.png')
sublevel = Image.open('../Assets/Levels/' + current_level + '/Sublevel.png')
overlay = Image.open('../Assets/Misc/Exclamation-Overlay.png')

# decrease the number of method arguments later...
images = [bg, player, sublevel, overlay]

global position
position = [int(bg.width/2), int(bg.height/2)]

global matrix

global mostrecent

if not debug:
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.gpio_slowdown = 2
    options.brightness=20
    options.hardware_mapping = 'adafruit-hat'
    options.daemon = False
    options.drop_privileges = False
    matrix = RGBMatrix(options = options)
else:
    resizefac=12
    matrix = TestScreen((64*resizefac, 32*resizefac))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = flask.Flask(__name__,
                static_url_path='',
                static_folder='../Web Interface/static',
                template_folder='../Web Interface/templates')

validmoves = ['left','right','up','down','lu','ru','ld','rd']

global started
started = False

@app.route("/")
def root():
    global started
    if not started:
        pass
        #graphics.displaycutscene('intro', matrix)
    started = True
    return flask.render_template("index.html")

@app.route('/<cmd>')
def command(cmd=None):
    global matrix
    global position
    global started

    global mostrecent

    response = cmd.lower()

    if response == 'esc':
        started = False
        position = [int(bg.width/2), int(bg.height/2)]
        matrix.Clear()
        matrix.SetImage(createqrcode.make())
        return "esc", 200, {'Content-Type': 'text/plain'}
    else:
        pass
        # mostrecent.cancel()
        # mostrecent = threading.Timer(45.0, command, ['esc'])
        # mostrecent.start()
    
    if response == 'center':
        pass
    
    elif response in validmoves:
        print("gasp")
        newpos = graphics.checkvalidmove(response, position, sublevel)
        if newpos:
            position = newpos[:]
    
    matrix.Clear()
    matrix.SetImage(graphics.frame(position,response, images))

    return response, 200, {'Content-Type': 'text/plain'}

# mostrecent = threading.Timer(45.0, command, ['esc'])
matrix.SetImage(createqrcode.make())
print("okay...")


if __name__ == "__main__":
    t = threading.Thread(target=app.run, kwargs={"host":"0.0.0.0", 'port':80, 'debug':True, 'threaded':True, 'use_reloader':False})
    t.start()
    # app.run(host="0.0.0.0", port=8000, debug=True, threaded=True, use_reloader=False)

matrix.check()

t.join()