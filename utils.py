from python_imagesearch.imagesearch import imagesearch_from_folder
from python_imagesearch.imagesearch import imagesearcharea
from python_imagesearch.imagesearch import imagesearch
import os
import pyautogui
import time
import cv2
import numpy as np
import random
import platform
import subprocess
from PIL import Image
import pytesseract
from pytesseract import image_to_string
import PIL.ImageOps  
import collections

#+-------BOARD--------+
#| 0| 1| 2| 3| 4| 5| 6| 
#| 7| 8| 9|10|11|12|13|    
#|14|15|16|17|18|19|20|  
#|21|22|23|24|25|26|27|  
#+--------------------+

#+--------------------------------BOARD------------------------------------+
#|[580,450],[680,450],[780,450],[880,450],[1020,450],[1120,450],[1220,450] | 
#|[600,500],[700,500],[800,500],[1000,500],[1100,500],[1200,500],[1300,500]|    
#|[550,600],[650,600],[750,600],[850,600],[1020,600],[1120,600],[1300,600] |  
#|[580,700],[700,700],[830,700],[970,700],[1110,700],[1220,700],[1350,700] |   
#+-------------------------------------------------------------------------+

#+--------------BENCH----------------+
#| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
#+-----------------------------------+


def initializeBoard():
    boardLine1 = [[580,420],[680,420],[780,420],[880,420],[1020,420],[1120,420],[1220,420]]
    boardLine2 = [[600,500],[700,500],[800,500],[1000,500],[1100,500],[1200,500],[1300,500]]
    boardLine3 = [[550,600],[650,600],[750,600],[850,600],[1020,600],[1120,600],[1300,600]]
    boardLine4 = [[550,650],[700,650],[830,650],[970,650],[1110,650],[1220,650],[1350,650]]

    completeBoard = boardLine1 + boardLine2 + boardLine3 + boardLine4
    return completeBoard
    
def initializeBench():
    benchBoard=[[426,775],[540,775],[662,775],[770,775],[880,775],[990,775],[1100,775],[1210,775],[1310,775]]
    return benchBoard

def initializeItems():
    itemBoard = [[296,760],[340,744],[314,714],[358,679],[338,660],[425,683],[398,652],[448,651],[404,610],[351,603]]
    return itemBoard
    
def initializeOrbPositions():
    orbPositions = [[1340,670],[599,231],[1253,246],[543,655],[929,438]]
    return orbPositions

def getCards():
    time1 = time.process_time()
    i=0
    cards = []
    path ="./assets/downNameCards/"
    path = path if path[-1] == '/' or '\\' else path+'/'
    valid_images = [".jpg", ".gif", ".png", ".jpeg"]

    img_rgb = pyautogui.screenshot(region=(450, 900, 1080, 1920))

    img_rgb = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1].lower() in valid_images]
    for file in files:
        template = cv2.imread(path+file, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.8)
        count = 0
        for pt in zip(*loc[::-1]):
            cards.append([file, pt])
            i=i+1
    print(str(time.process_time() - time1) + " seconds (optimized)")
    return cards   

def buyExp():
    pyautogui.mouseDown(x=365,y=967, button='left')
    pyautogui.mouseUp(x=365,y=967, button='left')

def reroll():
    pyautogui.mouseDown(x=365,y=1035, button='left')
    pyautogui.mouseUp(x=365,y=1035, button='left')

def testBoard(boardArray):
    for position in boardArray:
        pyautogui.dragTo(position[0], position[1], 0.13, button='left')
        pyautogui.mouseDown(x=position[0],y=position[1], button='left')
        pyautogui.mouseUp(x=position[0],y=position[1], button='left')
   
def getGold():
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    img = PIL.ImageOps.invert(pyautogui.screenshot(region=(870, 880, 35, 30)).convert('L'))
    ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(img.astype(np.uint8))
    return pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789.%')
    
def getExp():
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    img = PIL.ImageOps.invert(pyautogui.screenshot(region=(400, 880, 20, 30)).convert('L'))
    ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(img.astype(np.uint8))
    return pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789.%')

def getActualLevel():
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    img = PIL.ImageOps.invert(pyautogui.screenshot(region=(315, 880, 20, 30)).convert('L'))
    ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(img.astype(np.uint8))
    return pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789.%')
    
def printResume(benchChamps,boardChamps,gold,level,items):
    print("**************************")   
    print("BenchChamps: ")
    print(benchChamps)
    print("-------------------------")  
    print("BoardChamps: ")
    print(boardChamps)
    print("-------------------------")  
    #print("Items: ")
    #print(items)
    #print("-------------------------")   
    print("Gold: ")
    print(gold)
    print("-------------------------")   
    print("Level: ")
    print(level)
    
def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    print(image[-13:] + " not found, waiting...")
    if image != "./assets/inGameIcons/rounds/round_1/1_1_round.png":
        while pos[0] == -1:
            time.sleep(timesample)
            pos = imagesearch(image, precision)
    else:
        while pos[0] == -1:
            time.sleep(timesample)
            pyautogui.moveTo(978, 715)
            pyautogui.click()
            pos = imagesearch(image, precision)
    print(image[-13:] + " found.")
    print("-------------------------")  
    return pos