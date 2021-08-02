import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

import flask
from flask import Flask, render_template, Response, request, redirect, url_for

import createqrcode
import graphics

import os

current_level = "Demo Scene"

# load all of the images into memory for speed purposes?

bg = Image.open('/home/pi/QRPG/Assets/Levels/' + current_level + '/background.png')
player = Image.open('/home/pi/QRPG/Assets/Misc/Player.png')
sublevel = Image.open('/home/pi/QRPG/Assets/Levels/' + current_level + '/Sublevel.png')
overlay = Image.open('/home/pi/QRPG/Assets/Misc/Exclamation-Overlay.png')

# decrease the number of method arguments later...
images = [bg, player, sublevel, overlay]

global position
position = [int(bg.width/2), int(bg.height/2)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Options for RGB Matrix; appears to work well. Remember to run with "sudo" to avoid flickering

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 2
options.brightness=5
options.hardware_mapping = 'adafruit-hat'
options.daemon = False
options.drop_privileges = False

global matrix
matrix = RGBMatrix(options = options)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = flask.Flask(__name__,
                static_url_path='',
                static_folder='/home/pi/QRPG/Web Interface/static',
                template_folder='/home/pi/QRPG/Web Interface/templates')

validmoves = ['left','right','up','down','lu','ru','ld','rd']

global started
started = False

@app.route("/")
def root():
    global started
    if not started:
        graphics.displaycutscene('intro', matrix)
    started = True
    return flask.render_template("index.html")

@app.route('/<cmd>')
def command(cmd=None):
    global matrix
    global position
    global started
    response = cmd.lower()

    if response == 'esc':
        started = False
        matrix.Clear()
        matrix.SetImage(createqrcode.make())
        return "esc", 200, {'Content-Type': 'text/plain'}

    if response == 'center':
        pass
    
    elif response in validmoves:
        newpos = graphics.checkvalidmove(response, position, sublevel)
        if newpos:
            position = newpos[:]
    
    matrix.Clear()
    matrix.SetImage(graphics.frame(position,response, images),0,0)

    return response, 200, {'Content-Type': 'text/plain'}

matrix.SetImage(createqrcode.make())


#if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=False, threaded=True)