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

def moveItemToPlay(item,items,itemBoard,boardChamp, completeBoard):
    pyautogui.mouseDown(x=itemBoard[item[1]][0],y=itemBoard[item[1]][1], button='left')
    pyautogui.mouseUp(x=itemBoard[item[1]][0],y=itemBoard[item[1]][1], button='left')
    pyautogui.dragTo(completeBoard[boardChamp[1]][0], completeBoard[boardChamp[1]][1], 0.13, button='left')    
    itemBoard.remove(item)
    return items

def moveItemInBoard(item,items,itemBoard,finalPosition):
    pyautogui.mouseDown(x=itemBoard[item[1]][0],y=itemBoard[item[1]][1], button='left')
    pyautogui.mouseUp(x=itemBoard[item[1]][0],y=itemBoard[item[1]][1], button='left')
    pyautogui.dragTo(itemBoard[finalPosition][0], itemBoard[finalPosition][1], 0.13, button='left')
    items.append([item[0],finalPosition])
    items.remove(item)
    return items

def getCarouselItem():
    bowItem = imagesearch("./assets/carousel/bow.png")
    if bowItem[0] != -1:
        print("bowFound", bowItem[0], bowItem[1])
        #pyautogui.moveTo(bowItem[0], bowItem[1])
        pyautogui.mouseDown(x=bowItem[0], y=bowItem[1], button='right')
        pyautogui.mouseUp(x=bowItem[0], y=bowItem[1], button='right')
        pyautogui.mouseDown(x=bowItem[0], y=bowItem[1], button='right')
        pyautogui.mouseUp(x=bowItem[0], y=bowItem[1], button='right')
    else:
        print("bow not found")
        broadswordItem = imagesearch("./assets/carousel/broadsword.png")
        if broadswordItem[0] != -1:
            print("broadswordFound", broadswordItem[0], broadswordItem[1])
            pyautogui.mouseDown(x=broadswordItem[0], y=broadswordItem[1], button='right')
            pyautogui.mouseUp(x=broadswordItem[0], y=broadswordItem[1], button='right')
            pyautogui.mouseDown(x=broadswordItem[0], y=broadswordItem[1], button='right')
            pyautogui.mouseUp(x=broadswordItem[0], y=broadswordItem[1], button='right')
        else:
            print("broadsword not found")    
            tearItem = imagesearch("./assets/carousel/tear.png")
            if tearItem[0] != -1:
                print("tearFound", tearItem[0], tearItem[1])
                pyautogui.mouseDown(x=tearItem[0], y=tearItem[1], button='right')
                pyautogui.mouseUp(x=tearItem[0], y=tearItem[1], button='right')
                pyautogui.mouseDown(x=tearItem[0], y=tearItem[1], button='right')
                pyautogui.mouseUp(x=tearItem[0], y=tearItem[1], button='right')
            else:
                print("tear not found")    
                beltItem = imagesearch("./assets/carousel/belt.png")
                if beltItem[0] != -1:
                    print("beltFound", beltItem[0], beltItem[1])
                    pyautogui.mouseDown(x=beltItem[0], y=beltItem[1], button='right')
                    pyautogui.mouseUp(x=beltItem[0], y=beltItem[1], button='right')
                    pyautogui.mouseDown(x=beltItem[0], y=beltItem[1], button='right')
                    pyautogui.mouseUp(x=beltItem[0], y=beltItem[1], button='right')
                else:
                    print("belt not found")   

def getOrbs(positions):
    for position in positions:
        pyautogui.mouseDown(x=position[0], y=position[1], button='right')
        pyautogui.mouseUp(x=position[0], y=position[1], button='right')
        pyautogui.mouseDown(x=position[0], y=position[1], button='right')
        pyautogui.mouseUp(x=position[0], y=position[1], button='right')
        time.sleep(2)

def orderItems(itemBoard,items):
    pyautogui.mouseDown(x=599, y=231, button='right')
    pyautogui.mouseUp(x=599, y=231, button='right')
    pyautogui.mouseDown(x=599, y=231, button='right')
    pyautogui.mouseUp(x=599, y=231, button='right')
    time.sleep(1)
    pyautogui.mouseDown(x=itemBoard[0][0],y=itemBoard[0][1], button='left')
    pyautogui.mouseUp(x=itemBoard[0][0],y=itemBoard[0][1], button='left')
    pyautogui.dragTo(itemBoard[7][0], itemBoard[7][1], 0.13, button='left')
    
    pyautogui.mouseDown(x=itemBoard[1][0],y=itemBoard[1][1], button='left')
    pyautogui.mouseUp(x=itemBoard[1][0],y=itemBoard[1][1], button='left')
    pyautogui.dragTo(itemBoard[6][0], itemBoard[6][1], 0.13, button='left')
    
def checkItem(itemName,big_pic):
    small_pic = cv2.imread("./assets/items/"+itemName+".png")
    res = cv2.matchTemplate(big_pic,small_pic,cv2.TM_CCOEFF_NORMED)

    threshold = 0.75
    loc = np.where (res >= threshold)
    if list(loc[::-1][0]):
        x_coordinate = list(loc[::-1][0])[0]
        y_coordinate = list(loc[::-1][1])[0]
        return [x_coordinate,y_coordinate]
    else:
        return "notFound"
    
def getItems():
    items = []
    img2 = pyautogui.screenshot()
    img2.save("./screenshotItem.png")
    big_pic = cv2.imread("./screenshotItem.png")
    print("--- Items ---")
    itemList = ["mr","armor","ap","belt","bow","crit","broadsword","nature_force","neko","spatula","tear"]
    for possibleItem in itemList:
        itemPosition = checkItem(possibleItem,big_pic)
        if itemPosition != "notFound":
            items.append([possibleItem,itemPosition])
            print(possibleItem)  
    return items

def combineItems(items,completeBoard,boardChamps):
    for item in items:
        if item[0]=="broadsword":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="crit" or items[n][0]=="bow"  or items[n][0]=="mr" or items[n][0]=="tear":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'vayne' or boardChamp[0] == 'caitlyn':   
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                elif items[n][0]=="armor":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'irelia' or boardChamp[0] == 'wukong':   
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                n = n+1
                
        if item[0]=="bow":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="crit" or items[n][0]=="ap" or items[n][0]=="tear":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'vayne' or boardChamp[0] == 'caitlyn':   
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                elif items[n][0]=="armor":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'leona' or boardChamp[0] == 'fiora':   
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                n = n+1
                
        if item[0]=="armor":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="belt":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'vayne' or boardChamp[0] == 'caitlyn' or boardChamp[0] == 'ekko':   
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                elif items[n][0]=="crit" or items[n][0]=="tear":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'leona' or boardChamp[0] == 'fiora' or boardChamp[0] == 'wukong' or boardChamp[0] == 'vi':  
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True                          
                n = n+1
                
        if item[0]=="mr":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="armor" or items[n][0]=="tear" or items[n][0]=="crit" or items[n][0]=="ap":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'leona' or boardChamp[0] == 'fiora' or boardChamp[0] == 'wukong' or boardChamp[0] == 'vi':     
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True  
                n = n+1
                
        if item[0]=="ap":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="broadsword" or items[n][0]=="bow" or items[n][0]=="crit":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'vayne' or boardChamp[0] == 'caitlyn' or boardChamp[0] == 'ekko':    
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True  
                n = n+1
            
        if item[0]=="tear":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="crit":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'vayne' or boardChamp[0] == 'caitlyn' or boardChamp[0] == 'ekko':    
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                elif items[n][0]=="belt" or items[n][0]=="tear" or items[n][0]=="crit" or items[n][0]=="ap":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'leona' or boardChamp[0] == 'fiora' or boardChamp[0] == 'wukong' or boardChamp[0] == 'vi':     
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True  
                n = n+1
        if item[0]=="spatula":
            foundCombination = False
            n = 0
            while not foundCombination and n < len(items):
                if items[n][0]=="bow":
                    for boardChamp in boardChamps:
                        if boardChamp[0] == 'irelia':    
                            items = useItems(items, item,completeBoard,boardChamp,n)
                            foundCombination = True
                n = n+1

def useItems(items, item,completeBoard,boardChamp,n):
    if len(items)>=n:
        moveItemToPlay(item[1],completeBoard[boardChamp[1]])
        moveItemToPlay(items[n][1],completeBoard[boardChamp[1]])
        items.remove(item)
    return items