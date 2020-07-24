from python_imagesearch.imagesearch import imagesearch_from_folder
from python_imagesearch.imagesearch import imagesearcharea
from python_imagesearch.imagesearch import imagesearch
from python_imagesearch.imagesearch import imagesearch_loop
from utils import *
import os
import pyautogui
import time
from PIL import Image
import pytesseract
from pytesseract import image_to_string
import cv2
import PIL.ImageOps  
import numpy as np
   
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

opChamps = ['vayne','leona','vi','ekko','fiora','wukong','caitlyn','irelia']



