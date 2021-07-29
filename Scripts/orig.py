import flask
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

import flask
from flask import Flask, render_template, Response, request, redirect, url_for

import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


background_image = Image.open('colormap.png').convert('RGB')

global position
position = [background_image.width/2, background_image.height/2]


global matrix

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 2
options.brightness=25
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
options.daemon = False
options.drop_privileges = False

matrix = RGBMatrix(options = options)
matrix.SetImage(background_image, position[0], position[1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = flask.Flask(__name__)
@app.route("/")
def root():
    return flask.render_template("index.html")

@app.route('/<cmd>')
def command(cmd=None):
    global matrix
    global position
    response = ""

    if cmd.lower() == 'esc':
        matrix.Clear()
        matrix.SetImage(Image.open("qrcode.png").convert('RGB'))
        return "esc", 200, {'Content-Type': 'text/plain'}

    if cmd.lower() == 'center':
        response = "jump!"
    if cmd.lower() == 'left':
        response = "left"
        position[0] = position[0] -1
    if cmd.lower() == 'right':
        response = "right"
        position[0] = position[0] +1
    if cmd.lower() == 'up':
        response = "up"
        position[1] = position[1] -1
    if cmd.lower() == 'down':
        response = "down"
        position[1] = position[1] +1

    if cmd.lower() == 'lu':
        response = "left up"
        position = [position[0] -1, position[1] - 1]
    if cmd.lower() == 'ru':
        response = "right up"
        position = [position[0] +1, position[1] - 1]
    if cmd.lower() == 'ld':
        response = "left down"
        position = [position[0] -1, position[1] + 1]
    if cmd.lower() == 'rd':
        response = "right down"
        position = [position[0] +1, position[1] + 1]
    
    print(response)

    matrix.Clear()
    matrix.SetImage(background_image, -position[0], -position[1])
    matrix.SetPixel(32, 16, 0xFF, 0xFF, 0xFF)

    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, threaded=True)