from python_imagesearch.imagesearch import imagesearch_from_folder
from python_imagesearch.imagesearch import imagesearcharea
from python_imagesearch.imagesearch import imagesearch
from utils import *
from champUtils import * 
from itemUtils import *
import os
import pyautogui
import time
from PIL import Image
import pytesseract
from pytesseract import image_to_string
import cv2
import PIL.ImageOps  
import numpy as np


#img = pyautogui.screenshot(region=(290, 675, 45, 35))
#img.save("aaa.png")
#orderItems(itemBoard)
#items = checkItems()
#combineItems(items,completeBoard)

   
completeBoard = initializeBoard()
bench=initializeBench()
itemBoard=initializeItems()
orbPositions = initializeOrbPositions()
boardChamps = []
benchChamps = []
boughtOpChamps = []
champGoldValues = {'ahri':2,'annie':2,'aurelion':5,'bardo':3,'blitzcrank':2,'caitlyn':1,'cassiopeia':3,'darius':2,'ekko':5,'ezreal':3,'fiora':1,'fizz':4,'gangplank':5,'gnar':4,'graves':1,'illaoi':1,'irelia':4,'janna':5,
'j4':1,'mordekaiser':2,'rakan':2,'ashe':3,'karma':3,'jhin':4,'wukong':4,'jayce':3,'jinx':4,'kogmaw':2,'leona':1,'lucian':2,'lulu':5,'malph':1,'yi':3,'nautilus':2,'neeko':3,'nocturne':1,'poppy':1,'riven':4,
'rumble':3,'shaco':3,'shen':2,'soraka':4,'teemo':4,'thresh':5,'tf':1,'urgot':5,'vayne':3,'vi':3,'viktor':4,'xayah':1,'xerath':5,'xinzhao':2,'yasuo':3,'zed':2,'ziggs':1,'zoe':1}

opChamps = [['vayne',22],['leona',5],['vi',1],['ekko',27],['fiora',3],['wukong',2],['caitlyn',21],['irelia',11]]

#while True:
 #   time.sleep(1)
  #  print(pyautogui.position())

rounds = ["1_1_round","1_2_round","1_3_round","1_4_round","2_1_round","2_2_round","2_3_round","2_4_round","2_5_round","2_6_round","2_7_round","3_1_round","3_2_round","3_3_round","3_4_round","3_5_round","3_6_round","3_7_round","4_1_round","4_2_round","4_3_round","4_4_round","4_5_round","4_6_round","4_7_round","5_1_round","5_2_round","5_3_round","5_4_round","5_5_round","5_6_round","5_7_round","6_1_round","6_2_round","6_3_round","6_4_round","6_5_round","6_6_round","6_7_round"]

for round in rounds:
    phase = int(round[0])
    stage = int (round[2])
    if phase == 1:
        imagesearch_loop("./assets/inGameIcons/rounds/round_1/"+round+".png", 0.1)       
    elif phase == 2:
        imagesearch_loop("./assets/inGameIcons/rounds/round_2/"+round+".png", 0.1)  
    elif phase == 3:
        imagesearch_loop("./assets/inGameIcons/rounds/round_3/"+round+".png", 0.1) 
    elif phase == 4:
        imagesearch_loop("./assets/inGameIcons/rounds/round_4/"+round+".png", 0.1) 
    elif phase == 5:
        imagesearch_loop("./assets/inGameIcons/rounds/round_5/"+round+".png", 0.1)  
    elif phase == 6:
        imagesearch_loop("./assets/inGameIcons/rounds/round_6/"+round+".png", 0.1) 
    
    if phase == 1 and stage == 1:
        time.sleep(12)
        print("searching items...")
        getCarouselItem()
    elif phase == 1 and stage == 2:
        boardChamps.append(['X',24])
    elif (phase >= 2 and stage == 1):        
        level = int(getActualLevel())
        gold = int(getGold())
        possibleCards = getCards()

        boughtCards = buyNeededCards(possibleCards,gold,champGoldValues,benchChamps,boardChamps,opChamps,level)
        benchChamps = boughtCards[0]
        gold = boughtCards[1]
        boardChamps = boughtCards[2]
                    
        champs = locateChamps(benchChamps,boardChamps,completeBoard,bench,opChamps,level)
        boardChamps = champs[0]
        benchChamps = champs[1]
        if (int(getActualLevel())>len(boardChamps) and len(benchChamps)>0):
            boardChampPositions = []
            for boardChamp in boardChamps:
                boardChampPositions.append(boardChamp[1])
            
            minimumPosition = 10
            champ = []
            for benchChamp in benchChamps:
                if benchChamp[1]<minimumPosition:
                    minimumPosition = benchChamp[1]
                    champ = benchChamp
                    
            if 24 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],24])
                benchChamps.remove(champ) 
            elif 16 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],16])
                benchChamps.remove(champ) 
            elif 17 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],17])
                benchChamps.remove(champ) 
            elif 10 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],10])
                benchChamps.remove(champ) 
                
        sellUnknownBenchUnits(benchChamps, bench)                          
        boardChamps = sellUnknownBoardUnits(boardChamps,benchChamps,completeBoard)
        
        if gold > 14:
            reroll()
            time.sleep(0.5)
            possibleCards = getCards()

            boughtCards = buyNeededCards(possibleCards,gold,champGoldValues,benchChamps,boardChamps,opChamps,level)
            benchChamps = boughtCards[0]
            gold = boughtCards[1]
                        
            champs = locateChamps(benchChamps,boardChamps,completeBoard,bench,opChamps,level)
            boardChamps = champs[0]
            benchChamps = champs[1]
            if (int(getActualLevel())>len(boardChamps) and len(benchChamps)>0):
                boardChampPositions = []
                for boardChamp in boardChamps:
                    boardChampPositions.append(boardChamp[1])
                
                minimumPosition = 10
                champ = []
                for benchChamp in benchChamps:
                    if benchChamp[1]<minimumPosition:
                        minimumPosition = benchChamp[1]
                        champ = benchChamp
                        
                if 24 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],24])
                    benchChamps.remove(champ) 
                elif 16 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],16])
                    benchChamps.remove(champ) 
                elif 17 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],17])
                    benchChamps.remove(champ) 
                elif 10 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],10])
                    benchChamps.remove(champ) 
        
        time.sleep(2)    
        while gold > 53:
            buyExp()
            gold = gold - 4
                        
        getOrbs(orbPositions)
        sellUnknownBenchUnits(benchChamps,bench)    
        #orderItems(itemBoard)
        #items = getItems()
        #combineItems(items,completeBoard, boardChamps)
        items = ""
        printResume(benchChamps,boardChamps,gold,level,items)
    elif phase >= 2 and stage == 4:
        time.sleep(12)
        print("searching items...")
        #Search items
        getCarouselItem()
    else:
        level = int(getActualLevel())
        gold = int(getGold())
        possibleCards = getCards()

        boughtCards = buyNeededCards(possibleCards,gold,champGoldValues,benchChamps,boardChamps,opChamps,level)
        benchChamps = boughtCards[0]
        gold = boughtCards[1]
        boardChamps = boughtCards[2]
                    
        champs = locateChamps(benchChamps,boardChamps,completeBoard,bench,opChamps,level)
        boardChamps = champs[0]
        benchChamps = champs[1]
        if (int(getActualLevel())>len(boardChamps) and len(benchChamps)>0):
            boardChampPositions = []
            for boardChamp in boardChamps:
                boardChampPositions.append(boardChamp[1])
            
            minimumPosition = 10
            champ = []
            for benchChamp in benchChamps:
                if benchChamp[1]<minimumPosition:
                    minimumPosition = benchChamp[1]
                    champ = benchChamp
                    
            if 24 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],24])
                benchChamps.remove(champ) 
            elif 16 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],16])
                benchChamps.remove(champ) 
            elif 17 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],17])
                benchChamps.remove(champ) 
            elif 10 not in boardChampPositions and len(benchChamps)>0:
                boardChamps.append([champ[0],10])
                benchChamps.remove(champ) 
                
        sellUnknownBenchUnits(benchChamps, bench)                  
        boardChamps = sellUnknownBoardUnits(boardChamps,benchChamps,completeBoard)
        
        if gold > 14:
            reroll()
            time.sleep(0.5)
            possibleCards = getCards()

            boughtCards = buyNeededCards(possibleCards,gold,champGoldValues,benchChamps,boardChamps,opChamps,level)
            benchChamps = boughtCards[0]
            gold = boughtCards[1]
            boardChamps = boughtCards[2]
                        
            champs = locateChamps(benchChamps,boardChamps,completeBoard,bench,opChamps,level)
            boardChamps = champs[0]
            benchChamps = champs[1]
            if (int(getActualLevel())>len(boardChamps) and len(benchChamps)>0):
                boardChampPositions = []
                for boardChamp in boardChamps:
                    boardChampPositions.append(boardChamp[1])
                
                minimumPosition = 10
                champ = []
                for benchChamp in benchChamps:
                    if benchChamp[1]<minimumPosition:
                        minimumPosition = benchChamp[1]
                        champ = benchChamp
                        
                if 24 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],24])
                    benchChamps.remove(champ) 
                elif 16 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],16])
                    benchChamps.remove(champ) 
                elif 17 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],17])
                    benchChamps.remove(champ) 
                elif 10 not in boardChampPositions and len(benchChamps)>0:
                    boardChamps.append([champ[0],10])
                    benchChamps.remove(champ) 
        
        time.sleep(2)    
        while gold > 53:
            buyExp()
            gold = gold - 4
                        
        getOrbs(orbPositions)
        sellUnknownBenchUnits(benchChamps,bench)    
        #orderItems(itemBoard,items)
        #items = getItems()
        #combineItems(items,completeBoard, boardChamps)
        items = ""
        printResume(benchChamps,boardChamps,gold,level,items)
