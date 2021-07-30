import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

import flask
from flask import Flask, render_template, Response, request, redirect, url_for

import createqrcode
import graphics

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Options for RGB Matrix; appears to work well. Remember to run with "sudo" to avoid flickering

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 2
options.brightness=25
options.hardware_mapping = 'adafruit-hat'
options.daemon = False
options.drop_privileges = False

global matrix
matrix = RGBMatrix(options = options)
matrix.SetImage(graphics.frame(position,'up', images),0,0)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = flask.Flask(__name__,
                static_url_path='',
                static_folder='../Web Interface/static',
                template_folder='../Web Interface/templates')

validmoves = ['left','right','up','down','lu','ru','ld','rd']

@app.route("/")
def root():
    return flask.render_template("index.html")

@app.route('/<cmd>')
def command(cmd=None):
    global matrix
    global position
    response = cmd.lower()

    if response == 'esc':
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

if __name__ == "__main__":
    graphics.displaycutscene('intro', matrix)
    app.run(host="0.0.0.0", debug=False, threaded=True)