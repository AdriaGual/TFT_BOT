from python_imagesearch.imagesearch import imagesearch_from_folder
from python_imagesearch.imagesearch import imagesearcharea
import os
import pyautogui
import time
#im = pyautogui.screenshot(region=(0,0, 300, 400))
#im.save('./aaa.png')
#cards = imagesearch_from_folder('./assets/downCards/', 0.8)
time1 = time.process_time()
path ="./assets/downNameCards/"
print(path)
i=0
cards = {}
path = path if path[-1] == '/' or '\\' else path+'/'
valid_images = [".jpg", ".gif", ".png", ".jpeg"]
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1].lower() in valid_images]
for file in files:
    pos = imagesearcharea(path+file, 450, 900, 1080, 1920,0.8)
    #pos = imagesearch(path+file, 0.8)
    if pos[0] != -1:
        cards[i] = [file, pos]
        i=i+1

print("----------------")
print(cards)
print("----------------")
for i in cards:
  print("name: "+cards[i][0])
  print(cards[i][1])
  
print(str(time.process_time() - time1) + " seconds (optimized)")