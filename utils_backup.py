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
    orbPositions = [[1340,670],[1253,246],[599,231],[543,655],[929,438]]
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

def locateChamps(benchChamps,boardChamps,completeBoard,bench,opChamps):
    for benchChamp in benchChamps:
        if benchChamp[0]=='vayne' and not findBoardChamp(boardChamps, 'vayne') and not positionUsed(boardChamps,22):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[22])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],22])
        if benchChamp[0]=='caitlyn' and not findBoardChamp(boardChamps, 'caitlyn') and not positionUsed(boardChamps,21):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[21])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],21])
        if benchChamp[0]=='wukong' and not findBoardChamp(boardChamps, 'wukong') and not positionUsed(boardChamps,2):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[2])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],2])
        if benchChamp[0]=='vi' and not findBoardChamp(boardChamps, 'vi') and not positionUsed(boardChamps,1):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[1])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],1])
        if benchChamp[0]=='fiora' and not findBoardChamp(boardChamps, 'fiora') and not positionUsed(boardChamps,3):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[3])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],3])
        if benchChamp[0]=='leona' and not findBoardChamp(boardChamps, 'leona') and not positionUsed(boardChamps,5):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[5])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],5])
        if benchChamp[0]=='irelia' and not findBoardChamp(boardChamps, 'irelia') and not positionUsed(boardChamps,11):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[11])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],11])
        if benchChamp[0]=='ekko' and not findBoardChamp(boardChamps, 'ekko') and not positionUsed(boardChamps,27):
            moveBenchToPlay(bench[benchChamp[1]],completeBoard[27])
            benchChamps.remove(benchChamp)
            boardChamps.append([benchChamp[0],27])
    
    opChampNames = []
    for opChamp in opChamps:
        opChampNames.append(opChamp[0])
            
    for boardChamp in boardChamps:
        if boardChamp[0] not in opChampNames and len(benchChamps)>0:
            sellPlayUnit(completeBoard[boardChamp[1]])
            boardChamps.remove(boardChamp)
            boardChamps.append([benchChamps[0][0],24])
            benchChamps.remove(benchChamps[0])
        
    return [boardChamps, benchChamps]


def movePlayCharacter(initialPlayPosition, finalPlayPosition):
    pyautogui.mouseDown(x=initialPlayPosition[0],y=initialPlayPosition[1], button='left')
    pyautogui.mouseUp(x=initialPlayPosition[0],y=initialPlayPosition[1], button='left')
    pyautogui.dragTo(finalPlayPosition[0], finalPlayPosition[1], 0.13, button='left')
    
def moveBenchToPlay(benchPosition, playPosition):
    pyautogui.mouseDown(x=benchPosition[0],y=benchPosition[1], button='left')
    pyautogui.mouseUp(x=benchPosition[0],y=benchPosition[1], button='left')
    pyautogui.dragTo(playPosition[0], playPosition[1], 0.2, button='left')
    
def movePlayToBench(benchPosition,playPosition):
    pyautogui.mouseDown(x=playPosition[0],y=playPosition[1], button='left')
    pyautogui.mouseUp(x=playPosition[0],y=playPosition[1], button='left')
    pyautogui.dragTo(benchPosition[0], benchPosition[1], 0.13, button='left')   

def moveItemToPlay(itemPosition, playPosition):
    pyautogui.mouseDown(x=itemPosition[0],y=itemPosition[1], button='left')
    pyautogui.mouseUp(x=itemPosition[0],y=itemPosition[1], button='left')
    pyautogui.dragTo(playPosition[0], playPosition[1], 0.13, button='left')     

def moveItemInBoard(initialPosition, finalPosition):
    pyautogui.mouseDown(x=initialPosition[0],y=initialPosition[1], button='left')
    pyautogui.mouseUp(x=initialPosition[0],y=initialPosition[1], button='left')
    pyautogui.dragTo(finalPosition[0], finalPosition[1], 0.13, button='left')
     
def sellBenchUnit(benchPosition):
    pyautogui.mouseDown(x=benchPosition[0],y=benchPosition[1], button='left')
    pyautogui.mouseUp(x=benchPosition[0],y=benchPosition[1], button='left')
    pyautogui.dragTo(940, 1000, 0.13, button='left')

def sellPlayUnit(playPosition):
    pyautogui.mouseDown(x=playPosition[0],y=playPosition[1], button='left')
    pyautogui.mouseUp(x=playPosition[0],y=playPosition[1], button='left')
    pyautogui.dragTo(940, 1000, 0.13, button='left')

def sellAllPlayUnits(board):  
    for position in board:
        sellPlayUnit(position)
    
def sellAllBenchUnits(bench):  
    for position in bench:
        sellBenchUnit(position)

def sellNotBoughtBenchUnits(bench):  
    for position in bench:
        sellBenchUnit(position)

def buyExp():
    pyautogui.mouseDown(x=365,y=967, button='left')
    pyautogui.mouseUp(x=365,y=967, button='left')

def reroll():
    pyautogui.mouseDown(x=365,y=1035, button='left')
    pyautogui.mouseUp(x=365,y=1035, button='left')

def buyOnlyOP(cards,opChamps,gold,champGoldValues,benchChamps,boardChamps):
    boughtChamps=[]
    opChampsName = []
    for opChamp in opChamps:
        opChampsName.append(opChamp[0])
    
    for card in cards:
        if card[0][0:-4] in str(opChampsName):
            if champGoldValues[card[0][0:-4]] <= gold:
                gold = buyUnit(459+card[1][0],card[1][1]+798,gold,champGoldValues[card[0][0:-4]])
                boughtChamps.append(card[0][0:-4])
    
    if len(boughtChamps)!=0:
        for opChamp in boughtChamps:
            boardNumber = 0
            for boardChamp in boardChamps:
                if boardChamp[0]==card[0][0:-4]:
                    boardNumber = boardNumber+1
            benchNumber = 0
            for benchChamp in benchChamps:
                if benchChamp[0]==card[0][0:-4]:
                    benchNumber = benchNumber+1
            if benchNumber+boardNumber == 2:
                if boardNumber == 2:
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
                            minimumPosition = boardChap[1]
                    boardChamps.append([minimumBoardChamp[0]+2,minimumBoardChamp[1]])
                    boardChamps.remove(minimumBoardChamp)                       
                    boardChamps.remove(maximumBoardChamp)
                elif boardNumber == 1:
                    for benchChamp in benchChamps:
                        if benchChamp[0]==card[0][0:-4]:
                            benchChamps.remove(benchChamp)
                    for boardChamp in boardChamps:
                        if boardChamp[0]==card[0][0:-4]:
                            boardChamps.append([boardChamp[0]+2,boardChamp[1]])
                            boardChamps.remove(boardChamp)
                elif boardNumber == 0:
                    maximumBenchChamp = []
                    maximumPosition = -1
                    for benchChamp in benchChamps:
                        if benchChamp[1] > maximumBenchChamp and benchChamp[0]==card[0][0:-4]:
                            maximumBenchChamp = benchChamp
                            maximumPosition = benchChamp[1]
                    minimumBenchChamp = []
                    minimumPosition = 99
                    for benchChamp in benchChamps:
                        if benchChamp[1]<minimumBenchChamp and benchChamp[0]==card[0][0:-4]:
                            minimumBenchChamp = benchChamp
                            minimumPosition = benchChamp[1]
                    benchChamps.append([minimumBenchChamp[0]+2,minimumBenchChamp[1]])
                    benchChamps.remove(minimumBenchChamp)                         
                    benchChamps.remove(maximumBenchChamp)
                       
            benchChamps.append([opChamp,findAvailableBenchPosition(benchChamps)])
            gold = gold - champGoldValues[opChamp]
    return [benchChamps,gold,boardChamps]

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

def buyNeededCards(possibleCards,gold,champGoldValues,benchChamps,boardChamps,opChamps):
    boughtOpChamps = buyOnlyOP(possibleCards,opChamps,gold,champGoldValues,benchChamps,boardChamps)
    benchChamps = boughtOpChamps[0]
    boardChamps = boughtOpChamps[2]
    gold = boughtOpChamps[1]

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
    for boardChamp in boardChamps:
        if boardChamp[0]==champName:
            return True
    return False

def findBenchChamp(benchChamps,champName):
    for benchChamp in benchChamps:
        if benchChamp[0]==champName:
            return True
    return False

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

def buyUnit(posX,posY,gold, champGoldValue):
    pyautogui.mouseDown(x=posX,y=posY, button='left')
    pyautogui.mouseUp(x=posX,y=posY, button='left')
    pyautogui.mouseDown(x=posX,y=posY, button='left')
    pyautogui.mouseUp(x=posX,y=posY, button='left')  
    return gold - champGoldValue

def getOrbs(positions):
    for position in positions:
        pyautogui.mouseDown(x=position[0], y=position[1], button='right')
        pyautogui.mouseUp(x=position[0], y=position[1], button='right')
        pyautogui.mouseDown(x=position[0], y=position[1], button='right')
        pyautogui.mouseUp(x=position[0], y=position[1], button='right')
        time.sleep(2)
    
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

def cleanCarouselAndOrbCharacters(benchChamps,bench):
    print(benchChamps)
    usedPositions = []
    limit = 8
    if benchChamps:
        for benchChamp in benchChamps:
            usedPositions.append(benchChamp[1])
    
            missingNumbers = list(set(range(0, limit + 1)) - set(usedPositions))
            for missingNumber in missingNumbers:
                sellBenchUnit(bench[missingNumber])
        
    return benchChamps

def sellUnknownUnits(boardChamps,benchChamps,completeBoard,opChamps):
    for boardChamp in boardChamps:
        if boardChamp[1]==24 and len(benchChamps)>0:  
            if boardChamp[0]=='X':
                sellPlayUnit(completeBoard[24])
                boardChamps.remove(boardChamp)
                boardChamps.append([benchChamps[0][0],24])
                benchChamps.remove(benchChamps[0])
            elif isAnOPChamp(opChamps, boardChamp[0]) != -1:
                movePlayCharacter(completeBoard[24], completeBoard[isAnOPChamp(opChamps, boardChamp[0])])
        elif boardChamp[1]==16 and len(benchChamps)>0:
            if boardChamp[0]=='X':
                sellPlayUnit(completeBoard[16])
                boardChamps.remove(boardChamp)
                boardChamps.append([benchChamps[0][0],16])
                benchChamps.remove(benchChamps[0])
            elif isAnOPChamp(opChamps, boardChamp[0]) != -1:
                movePlayCharacter(completeBoard[16], completeBoard[isAnOPChamp(opChamps, boardChamp[0])])
        elif boardChamp[1]==17 and len(benchChamps)>0 and boardChamp[0]=='X':
            if boardChamp[0]=='X':
                sellPlayUnit(completeBoard[17])
                boardChamps.remove(boardChamp)
                boardChamps.append([benchChamps[0][0],17])
                benchChamps.remove(benchChamps[0])
            elif isAnOPChamp(opChamps, boardChamp[0]) != -1:
                movePlayCharacter(completeBoard[17], completeBoard[isAnOPChamp(opChamps, boardChamp[0])])
        elif boardChamp[1]==10 and len(benchChamps)>0 and boardChamp[0]=='X':
            if boardChamp[0]=='X':
                sellPlayUnit(completeBoard[10])
                boardChamps.remove(boardChamp)
                boardChamps.append([benchChamps[0][0],10])
                benchChamps.remove(benchChamps[0])
            elif isAnOPChamp(opChamps, boardChamp[0]) != -1:
                movePlayCharacter(completeBoard[10], completeBoard[isAnOPChamp(opChamps, boardChamp[0])])
            
    return [boardChamps, benchChamps]
    
def isAnOPChamp(opChamps, champName):
    opChampNames = []
    
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
def orderItems(itemBoard):
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
    print(items)
    print(item)
    print(boardChamp)
    print(n)
    if len(items)>=n:
        moveItemToPlay(item[1],completeBoard[boardChamp[1]])
        moveItemToPlay(items[n][1],completeBoard[boardChamp[1]])
        items.remove(item)
    return items
                

def printResume(benchChamps,boardChamps,gold,level,items):
    print("**************************")   
    print("BenchChamps: ")
    print(benchChamps)
    print("-------------------------")  
    print("BoardChamps: ")
    print(boardChamps)
    print("-------------------------")  
    print("Items: ")
    print(items)
    print("-------------------------")   
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