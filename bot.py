from python_imagesearch.imagesearch import imagesearch
from python_imagesearch.imagesearch import imagesearch_loop
from python_imagesearch.imagesearch import imagesearch_from_folder
from utils import getCarouselItem
from utils import getCards
from utils import buyOnlyOP
import pyautogui
import time

############## START LOL ##############

#Launch LoL
print('searching lol...')
lol_icon = imagesearch_loop("./assets/outGameIcons/lol_icon.png", 1)
pyautogui.moveTo(lol_icon[0]+20, lol_icon[1]+20)
pyautogui.doubleClick()
print("starting lol...")

#Play Icon
play_menu = imagesearch_loop("./assets/outGameIcons/play_menu.png", 1)
pyautogui.moveTo(play_menu[0]+20, play_menu[1]+20)
pyautogui.click()
print("searching playmode...")

#Choose PVP
pvp_text = imagesearch_loop("./assets/outGameIcons/pvp_text.png", 1)
pyautogui.moveTo(pvp_text[0]+10, pvp_text[1]+10)
pyautogui.click()
print("pvp")

#Confirm Icon (NEEDS TO CHOSE RANKED)
confirm_icon = imagesearch_loop("./assets/outGameIcons/confirm_icon.png", 1)
pyautogui.moveTo(confirm_icon[0]+20, confirm_icon[1]+20)
pyautogui.click()

#Find match
find_match_icon = imagesearch_loop("./assets/outGameIcons/find_match_icon.png", 1)
pyautogui.moveTo(find_match_icon[0]+20, find_match_icon[1]+20)
pyautogui.click()

#Accept found match
accept_icon = imagesearch_loop("./assets/outGameIcons/accept_icon.png", 1)
pyautogui.moveTo(accept_icon[0]+20, accept_icon[1]+20)
pyautogui.click()

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
opChamps = ['j4','mordekaiser','rakan','ashe','karma','jhin','wukong']

############## START GAME ##############
round_1_1 = imagesearch_loop("./assets/inGameIcons/rounds/round_1/1_1_round.png", 1)

#-- ROUND 1 1 CAROUSEL --#

#Wait 120 seconds
time.sleep(12)
print("searching items...")
#Search items
getCarouselItem()

round_1_3 = imagesearch_loop("./assets/inGameIcons/rounds/round_1/1_3_round.png", 1)  

#-- ROUND 1 3 --#            



#Look Cards
sellPlayUnit(completeBoard[24])
sellAllBenchUnits(bench)
possibleCards = getCards()
boughtOpChamps = buyOnlyOP(possibleCards,opChamps)
if len(boughtOpChamps)==0:
    buyAllCards(possibleCards)
    
for opChamp in boughtOpChamps:
    benchChamps.append([opChamp,len(benchChamps)])
    
print(benchChamps)
getItems()
round_1_4 = imagesearch_loop("./assets/inGameIcons/rounds/round_1/1_4_round.png", 1)  
