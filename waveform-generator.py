import argparse, math, PIL
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description='Generates a waveform from a .wav file.')
parser.add_argument("-f", "--file", help="File path.", type=str)
parser.add_argument("-d", "--dir", help="Save path.", type=str)
parser.add_argument("-c", "--count", help="Bar count.", type=int)
parser.add_argument("-s", "--show", help="Show image at completion.", action="store_true")

args = parser.parse_args()


def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner


def round_rectangle(size, radius, fill):
    """Draw a rounded rectangle"""
    width, height = size
    rectangle = Image.new('RGBA', size, fill)
    corner = round_corner(radius, fill)
    rectangle.paste(corner, (0, 0))
    rectangle.paste(corner.rotate(90), (0, height - radius))  # Rotate the corner and paste it
    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))
    return rectangle

samplerate, data = wavfile.read(args.file)
#print("number of channels = {}".format(data.shape[1]))
length = data.shape[0]
bar_count = args.count
chunk = length/bar_count
max_amplitude = np.max(data)

# Make image
bar_size = 10
bar_margin = 5
img_height = 150

im = Image.new('RGBA', (2*bar_size + bar_size*bar_count + bar_margin*(bar_count-1),img_height), (0,0,0,0))
#print("chunk={}".format(chunk))
#print("length={}".format(length))
amps = []
for i in range(args.count):
    coord1 = math.floor(chunk*i)
    coord2 = math.floor(chunk*(i+1))
    #print(coord1)
    amp = np.max(data[coord1:coord2])/max_amplitude
    amps.append(amp)
    #print(amp)
    # Draw rectangles
    bar_height = math.floor(img_height*amp)
    paste_height = math.floor((img_height-bar_height)/2)
    #print(paste_height)
    im.paste(round_rectangle((bar_size, bar_height), 5, "white"),(bar_size+bar_size*i+bar_margin*(i),paste_height))




im.save(args.dir+r"\output.png")
if args.show:
    im.show()
