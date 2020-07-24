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

def locateChamps(benchChamps,boardChamps,completeBoard,bench,opChamps,level):
    for benchChamp in benchChamps:
        if benchChamp[0]=='vayne' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'vayne') and not positionUsed(boardChamps,22):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 22,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='caitlyn' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'caitlyn') and not positionUsed(boardChamps,21):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 21,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='wukong' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'wukong') and not positionUsed(boardChamps,2):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 2,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='vi' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'vi') and not positionUsed(boardChamps,1):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 1,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='fiora' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'fiora') and not positionUsed(boardChamps,3):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 3,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='leona' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'leona') and not positionUsed(boardChamps,5):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 5,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='irelia' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'irelia') and not positionUsed(boardChamps,11):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 11,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
        if benchChamp[0]=='ekko' and level > len(boardChamps) and not findBoardChamp(boardChamps, 'ekko') and not positionUsed(boardChamps,27):
            locatedChamps = moveBenchToBoard(benchChamp,boardChamps,benchChamps, 27,completeBoard,bench)
            boardChamps = locatedChamps[0]
            benchChamps = locatedChamps[1]
    
    opChampNames = []
    for opChamp in opChamps:
        opChampNames.append(opChamp[0])
            
    for boardChamp in boardChamps:
        if boardChamp[0] not in opChampNames and len(benchChamps)>0:
            boardChamps = sellBoardUnit(boardChamp,boardChamps,completeBoard)
            minimumChamp = []
            minimumPosition = 99
            for benchChamp in benchChamps:
                if benchChamp[1]<minimumPosition:
                    minimumPosition = benchChamp[1]
                    minimumChamp = benchChamp     
            boardChamps.append([minimumChamp[0],24])
            benchChamps.remove(minimumChamp)
        if boardChamp[0] in opChampNames:
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            boardPosition = -1
            for opChamp in opChamps:
                if opChamp[0]==boardChamp[0] and opChamp[1]!=boardChamp[1]:
                    boardPosition = opChamp[1]
            if boardPosition >= 0:
                boardChamps = moveBoardCharacter(boardChamp,boardChamps,boardPosition,completeBoard)
        
    return [boardChamps, benchChamps]


def moveBoardCharacter(champ,boardChamps,finalBoardPosition,completeBoard):
    pyautogui.mouseDown(x=completeBoard[champ[1]][0],y=completeBoard[champ[1]][1], button='left')
    pyautogui.mouseUp(x=completeBoard[champ[1]][0],y=completeBoard[champ[1]][1], button='left')
    pyautogui.dragTo(completeBoard[finalBoardPosition][0], completeBoard[finalBoardPosition][1], 0.13, button='left')
    boardChamps.append([champ[0],finalBoardPosition])
    boardChamps.remove(champ)
    return boardChamps
    
def moveBenchToBoard(champ,boardChamps,benchChamps, finalBoardPosition,completeBoard,bench):
    pyautogui.mouseDown(x=bench[champ[1]][0],y=bench[champ[1]][1], button='left')
    pyautogui.mouseUp(x=bench[champ[1]][0],y=bench[champ[1]][1], button='left')
    pyautogui.dragTo(completeBoard[finalBoardPosition][0],completeBoard[finalBoardPosition][1], 0.2, button='left')
    boardChamps.append([champ[0],finalBoardPosition])
    benchChamps.remove(champ)
    return [boardChamps,benchChamps]
    
def moveBoardToBench(champ,boardChamps,benchChamps, finalBenchPosition,completeBoard,bench):
    pyautogui.mouseDown(x=completeBoard[champ[1]][0],y=completeBoard[champ[1]][1], button='left')
    pyautogui.mouseUp(x=completeBoard[champ[1]][0],y=completeBoard[champ[1]][1], button='left')
    pyautogui.dragTo(bench[finalBenchPosition][0],bench[finalBenchPosition][1], 0.13, button='left')   
    benchChamps.append([champ[0],finalBoardPosition])
    boardChamps.remove(champ)
    return [boardChamps,benchChamps]
     
def sellBenchUnit(champ,benchChamps,bench):
    pyautogui.mouseDown(x=bench[champ[1]][0],y=bench[champ[1]][1], button='left')
    pyautogui.mouseUp(x=bench[champ[1]][0],y=bench[champ[1]][1], button='left')
    pyautogui.dragTo(940, 1000, 0.13, button='left')
    benchChamps.remove(champ)
    return benchChamps
    
def sellUnknownBenchUnit(position, bench):
    pyautogui.mouseDown(x=bench[position][0],y=bench[position][1], button='left')
    pyautogui.mouseUp(x=bench[position][0],y=bench[position][1], button='left')
    pyautogui.dragTo(940, 1000, 0.13, button='left')

def sellBoardUnit(champ,boardChamps,completeBoard):
    pyautogui.mouseDown(x=completeBoard[champ[1]][0],y=completeBoard[champ[1]][1], button='left')
    pyautogui.mouseUp(x=completeBoard[champ[1]][0],y=completeBoard[champ[1]][1], button='left')
    pyautogui.dragTo(940, 1000, 0.13, button='left')
    boardChamps.remove(champ)
    return boardChamps
    
def sellAllNotOPUnits(benchChamps, bench, opChamps):  
    opChampNames = getOpChampNames(opChamps)
    for benchChamp in benchChamps:
        if benchChamp[0] not in opChampNames:
            benchChamps = sellBenchUnit(benchChamp,benchChamps,bench)
    return benchChamps
    
    
def buyUnit(posX,posY,champName,benchChamps):
    pyautogui.mouseDown(x=posX,y=posY, button='left')
    pyautogui.mouseUp(x=posX,y=posY, button='left')
    pyautogui.mouseDown(x=posX,y=posY, button='left')
    pyautogui.mouseUp(x=posX,y=posY, button='left') 
    benchChamps.append([champName,findAvailableBenchPosition(benchChamps)])
    return benchChamps  

def buyARandomChamp(possibleCards,boughtChamps,benchChamps,boardChamps):
    for card in possibleCards:
        n= 0
        found = False
        while n < len(boughtChamps) and not found:
            if card[0]!=boughtChamps[0][0] and card[1]!=boughtChamps[0][1]:
                benchChamps = buyUnit(459+card[1][0],card[1][1]+798,card[0][0:-4],benchChamps)
                boardChamps.append([benchChamps[0][0],findAvailableBoardPosition(boardChamps)])
                benchChamps.remove(benchChamps[0])
                boughtChamps.append(card)
                found = True
                n= n+1
                
    return [benchChamps,boughtChamps,boardChamps]

def buyOnlyOP(cards,opChamps,gold,champGoldValues,benchChamps,boardChamps):
    boughtChamps=[]
    opChampsName = getOpChampNames(opChamps)
    
    
    for card in cards:
        if card[0][0:-4] in str(opChampsName):
            benchChamps = buyUnit(459+card[1][0],card[1][1]+798,card[0][0:-4],benchChamps)
            boughtChamps.append(card)
    
        if len(boughtChamps) > 0:
            for opChamp in boughtChamps:
                boardNumber = 0
                for boardChamp in boardChamps:
                    if boardChamp[0]==card[0][0:-4]:
                        boardNumber = boardNumber+1
                benchNumber = 0
                for benchChamp in benchChamps:
                    if benchChamp[0]==card[0][0:-4]:
                        benchNumber = benchNumber+1     
                if benchNumber+boardNumber == 3:
                    if boardNumber == 3:
                        minimumBoardChamp = []
                        minimumPosition = 99
                        for boardChamp in boardChamps:
                            if boardChamp[1] < minimumPosition and boardChamp[0]==card[0][0:-4]:
                                minimumBoardChamp = boardChamp
                                minimumPosition = boardChamp[1]
                        
                        for boardChamp in boardChamps:
                            if boardChamp[0]==minimumBoardChamp[0] and boardChamp[1]!=minimumBoardChamp[1]:
                                boardChamps.remove(boardChamp)
                                
                    elif boardNumber == 2:
                        maximumBoardChamp = []
                        maximumPosition = -1
                        for boardChamp in boardChamps:
                            if boardChamp[1]>maximumPosition and boardChamp[0]==card[0][0:-4]:
                                maximumBoardChamp = boardChamp
                                maximumPosition = boardChamp[1]
                        minimumBoardChamp = []
                        minimumPosition = 99
                        for boardChamp in boardChamps:
                            if boardChamp[1]<minimumPosition and boardChamp[0]==card[0][0:-4]:
                                minimumBoardChamp = boardChamp 
                                minimumPosition = boardChamp[1]
                        boardChamps.append([minimumBoardChamp[0]+'2',minimumBoardChamp[1]])
                        boardChamps.remove(minimumBoardChamp)                       
                        boardChamps.remove(maximumBoardChamp)
                    elif boardNumber == 1:
                        for benchChamp in benchChamps:
                            if benchChamp[0]==card[0][0:-4]:
                                benchChamps.remove(benchChamp)
                        for boardChamp in boardChamps:
                            if boardChamp[0]==card[0][0:-4]:
                                boardChamps.append([boardChamp[0]+'2',boardChamp[1]])
                                boardChamps.remove(boardChamp)
                    elif boardNumber == 0:
                        maximumBenchChamp = []
                        maximumPosition = -1
                        for benchChamp in benchChamps:
                            if benchChamp[1] > maximumPosition and benchChamp[0]==card[0][0:-4]:
                                maximumBenchChamp = benchChamp
                                maximumPosition = benchChamp[1]
                        minimumBenchChamp = []
                        minimumPosition = 99
                        for benchChamp in benchChamps:
                            if benchChamp[1]<minimumPosition and benchChamp[0]==card[0][0:-4]:
                                minimumBenchChamp = benchChamp
                                minimumPosition = benchChamp[1]
                        benchChamps.append([minimumBenchChamp[0]+'2',minimumBenchChamp[1]])
                        benchChamps.remove(minimumBenchChamp)                         
                        benchChamps.remove(maximumBenchChamp)
                       
    return [benchChamps,gold,boardChamps,boughtChamps]

def buyLevelUps(possibleCards,gold,champGoldValues,benchChamps,boardChamps):
    boughtChamps=[]
    for card in possibleCards:
        n = 0
        for boardChamp in boardChamps:
            if boardChamp[0]==card[0][0:-4]:
                n=n+1
        for benchChamp in benchChamps:
            if benchChamp[0]==card[0][0:-4]:
                n=n+1
        for otherCards in possibleCards:
            if card[0][0:-4] == otherCards[0][0:-4] and card[1] != otherCards[1]:
                n = n+1        
        if n >= 2 and champGoldValues[card[0][0:-4]] <= gold:
            gold = buyUnit(459+card[1][0],card[1][1]+798,gold,champGoldValues[card[0][0:-4]])
            boughtChamps.append(card[0][0:-4])
            
    if len(boughtChamps)!=0:
        for levelUpChamp in boughtChamps:
            benchChamps.append([levelUpChamp,findAvailableBenchPosition(benchChamps)])
            gold = gold - champGoldValues[levelUpChamp]        
    return [benchChamps,gold]
    
def buyPairs(possibleCards,gold,champGoldValues,benchChamps,boardChamps):
    boughtChamps=[]
    for card in possibleCards:
        n = 0
        for otherCards in possibleCards:
            if card[0][0:-4] == otherCards[0][0:-4] and card[1] != otherCards[1]:
                n = n+1
        if n == 1 and champGoldValues[card[0][0:-4]] <= gold:
            gold = buyUnit(459+card[1][0],card[1][1]+798,gold,champGoldValues[card[0][0:-4]])
            boughtChamps.append(card[0][0:-4])
    
    for card in possibleCards:
        n = 0
        for boardChamp in boardChamps:
            if boardChamp[0]==card[0][0:-4]:
                n=n+1
        
        for benchChamp in benchChamps:
            if benchChamp[0]==card[0][0:-4]:
                n=n+1
        if n == 1 and champGoldValues[card[0][0:-4]]*2 <= gold:
            gold = buyUnit(459+card[1][0],card[1][1]+798,gold,champGoldValues[card[0][0:-4]])
            boughtChamps.append(card[0][0:-4])
            
    if len(boughtChamps)!=0:
        for pairChamp in boughtChamps:
            benchChamps.append([pairChamp,findAvailableBenchPosition(benchChamps)])
            gold = gold - champGoldValues[pairChamp]              
            
    return [benchChamps,gold]  
    
def buyAllCards(cards,gold,champGoldValues,benchChamps):
    boughtChamps=[]
    for card in cards:
        if champGoldValues[card[0][0:-4]] <= gold:
            gold = buyUnit(459+card[1][0],card[1][1]+798,gold,champGoldValues[card[0][0:-4]])
            boughtChamps.append(card[0][0:-4])
            
    if len(boughtChamps)!=0:
        for trashChamp in boughtChamps:
            benchChamps.append([trashChamp,findAvailableBenchPosition(benchChamps)])
            gold = gold - champGoldValues[trashChamp]              
    return [benchChamps,gold]  

def buyNeededCards(possibleCards,gold,champGoldValues,benchChamps,boardChamps,opChamps,level):
    boughtOpChamps = buyOnlyOP(possibleCards,opChamps,gold,champGoldValues,benchChamps,boardChamps)
    benchChamps = boughtOpChamps[0]
    boardChamps = boughtOpChamps[2]
    boughtChamps = boughtOpChamps[3]
    gold = boughtOpChamps[1]
    n = len(benchChamps)+len(boardChamps)
    while n < level:
        boughtRandomChamp = buyARandomChamp(possibleCards,boughtChamps,benchChamps,boardChamps)
        benchChamps = boughtRandomChamp[0]
        boughtChamps = boughtRandomChamp[1]
        boardChamps = boughtRandomChamp[2]
        n = n+1
    
    #if not boughtOpChamps[0]:
     #   boughtLevelUps = buyLevelUps(possibleCards,gold,champGoldValues,benchChamps,boardChamps)
     #   benchChamps = boughtLevelUps[0]
     #   gold = boughtLevelUps[1]
        
     #   if not boughtLevelUps[0]:
      #      boughtPairs = buyPairs(possibleCards,gold,champGoldValues,benchChamps,boardChamps)
      #      benchChamps = boughtPairs[0]
      #      gold = boughtPairs[1]
            
        #    if not boughtLevelUps[0]:
        #        boughtTrash = buyAllCards(possibleCards,gold,champGoldValues,benchChamps)
         #       benchChamps = boughtTrash[0]
         #       gold = boughtTrash[1]
    
    return [benchChamps, gold,boardChamps]
   

def findAvailableBenchPosition(benchChamps):
    if not benchChamps:
        return 0
    else:
        usedPositions = []
        limit = 9
        for benchChamp in benchChamps:
            usedPositions.append(benchChamp[1])
        missingNumbers = list(set(range(0, limit + 1)) - set(usedPositions))
        return missingNumbers[0]
        
def findAvailableBoardPosition(boardChamps):
    if not boardChamps:
        return 0
    else:
        usedPositions = []
        limit = 27
        for boardChamp in boardChamps:
            usedPositions.append(boardChamp[1])
        missingNumbers = list(set(range(0, limit + 1)) - set(usedPositions))
        return missingNumbers[0]

def findBoardChamp(boardChamps,champName):
    n = 0
    for boardChamp in boardChamps:
        if boardChamp[0]==champName:
            n = n+1
    return n

def findBenchChamp(benchChamps,champName):
    n = 0
    for benchChamp in benchChamps:
        if benchChamp[0]==champName:
            n = n+1
    return n
    
def testBoard(boardArray):
    for position in boardArray:
        pyautogui.dragTo(position[0], position[1], 0.13, button='left')
        pyautogui.mouseDown(x=position[0],y=position[1], button='left')
        pyautogui.mouseUp(x=position[0],y=position[1], button='left')


def sellUnknownBenchUnits(benchChamps,bench):
    usedPositions = []
    limit = 8
    if benchChamps:
        for benchChamp in benchChamps:
            usedPositions.append(benchChamp[1])
    
        missingNumbers = list(set(range(0, limit + 1)) - set(usedPositions))
        
        for missingNumber in missingNumbers:
            sellUnknownBenchUnit(missingNumber, bench)   

def sellUnknownBoardUnits(boardChamps,benchChamps,completeBoard):
    print('sellUnknownBoardUnits')
    for boardChamp in boardChamps:
        if boardChamp[0]=='X' and len(benchChamps)>0:
            print(boardChamp[0])
            print(len(benchChamps))
            boardChamps = sellBoardUnit(boardChamp,boardChamps,completeBoard)
    return boardChamps
    
def isAnOPChamp(opChamps, champName):
    for opChamp in opChamps:
        if opChamp[0]==champName:
            return opChamp[1]
            
    return -1    

def isChampInBench(benchChamps,champ):
    n = 0
    for benchChamp in benchChamps:
        if benchChamp[0] == champ:
            n = n+1
    return n

def isChampInBoard(boardChamps,champ):
    n = 0
    for boardChamp in boardChamps:
        if boardChamp[0] == champ:
            n = n+1
    return n
    
def positionUsed(boardChamps,position):
    used = False
    for boardChamp in boardChamps:
        if boardChamp[1]==position:
            used = True 
    return used
    
def getOpChampNames(opChamps):
    opChampNames = []
    for opChamp in opChamps:
        opChampNames.append(opChamp[0])
    return opChampNames