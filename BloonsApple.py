import asyncio
import time
from PIL import Image
import json
import pyautogui

import sys
import os

Total_Frames = 6515

ASCII_CHARS = ['0','0','0','0','0','0','0','1','1','1','1','1']
ASCII_CHARS.reverse()
ASCII_CHARS = ASCII_CHARS[::-1]

global i
global oldtime
global newtime

oldtime = 0

WIDTH = 10
HEIGHT = 6

TIMEOUT = 1/((int(Total_Frames)+1)/220)*18

def resize(image, new_width=WIDTH):
    (old_width, old_height) = image.size
    #aspect_ratio = #float(old_height)/float(old_width)
    new_height = HEIGHT #int((aspect_ratio * new_width)/2)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

def greyscale(image):
    return image.convert('L')

def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

def do(image, new_width=WIDTH):
    image = resize(image)
    image = greyscale(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index+int(new_width)] for index in range(0, len_pixels, int(new_width))]

    return '\n'.join(new_image)

def backspace():
    pyautogui.keyDown('ctrl')
    pyautogui.press('e')
    pyautogui.keyUp('ctrl')

def qkey():
    pyautogui.keyDown('ctrl')
    pyautogui.press('q')
    pyautogui.keyUp('ctrl')

def runner(path, x):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        return
        
    image = do(image)
    time.sleep(2)
    pyautogui.click(59, 376)
        
    i = 0
    y = 0
    useful_height = int(HEIGHT)
    useful_width = WIDTH
    for thing in image:
        if thing == "1":
            #print("dart")
            qkey()
            pyautogui.click()
            tempx, tempy = pyautogui.position()
            pyautogui.moveTo(tempx+65, tempy, 0)

        elif thing == "0":
            #print("not dart")
            tempx, tempy = pyautogui.position()
            pyautogui.moveTo(tempx+65, tempy, 0)

        else:
            #print("else statement")
            pass
        
        i += 1
        if i == useful_width+1:
            i = 0
            y += 1
            pyautogui.moveTo(59, 376+(y*65), 0)
    
    time.sleep(1)
    pyautogui.press("f12")
    time.sleep(1)

    pyautogui.click(59, 376)

    i = 0
    y = 0
    useful_height = int(HEIGHT)
    useful_width = WIDTH
    for thing in image:
        if thing == "1":
            pyautogui.click()
            backspace()
            tempx, tempy = pyautogui.position()
            pyautogui.moveTo(tempx+65, tempy, 0)

        elif thing == "0":
            tempx, tempy = pyautogui.position()
            pyautogui.moveTo(tempx+65, tempy, 0)

        else:
            pass
        
        i += 1
        if i == useful_width+1:
            i = 0
            y += 1
            pyautogui.moveTo(59, 376+(y*65), 0)

    return image

frames = []

for x in range(2, 5584, 2):
    path = "frames/frame"+str(x)+".png"
    runner(path, x)
#print(frames)

#i = 1
#for i in range(1, 2, 1):
#    fillcommand = []
#    
#    print(f"{frames}")