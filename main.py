import cv2
import math
import cvzone
import numpy as np
import streamlit as st
from PIL import ImageGrab
from ultralytics import YOLO
import threading
from setup import *


model = YOLO("playingCards.pt")
classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']

A = 127
S8 = 182

card_positions = [[S8 + (138 *3),110],[S8 + (138 *2),110],[S8 + 138,110],[S8,110],#10
                  [A + (137 * 3),48],[A + (137 * 2),48],[A + 137,48],[A,48], #2
                  [A + (137 * 3),90],[A + (137 * 2),90],[A + 137,90],[A,90],#3
                  [A + (137 * 3),133],[A + (137 * 2),133],[A + 137,133],[A,133],#4
                  [A + (137 * 3),175],[A + (137 * 2),175],[A + 137,175],[A,175],#5
                  [A + (137 * 3),218],[A + (137 * 2),218],[A + 137,218],[A,218],#6
                  [A + (137 * 3),260],[A + (137 * 2),260],[A + 137,260],[A,260],#7
                  [S8 + (138 *3),28],[S8 + (138 *2),28],[S8 + 138,28],[S8,28],#8
                  [S8 + (138 *3),70],[S8 + (138 *2),70],[S8 + 138,70],[S8,70],#9
                  [A + (137 * 3) ,8],[A + (137 *2) ,8],[A + 137, 8],[A,8],#A
                  [S8 + (138 *3),155],[S8 + (138 *2),155],[S8 + 138,155],[S8,155],#j
                  [S8 + (138 *3),238],[S8 + (138 *2),238],[S8 + 138,238],[S8,238],#K
                  [S8 + (138 *3),196],[S8 + (138 *2),196],[S8 + 138,196],[S8,196]]#Q

# # Khởi tạo một dictionary để lưu trữ vị trí của các lá bài
# card_positions = {card_name: False for card_name in classNames}


cards = dict(zip(classNames, card_positions))
# print(cards)

        



f_height = 405 
f_width = 520 

def capture_screen():
     # Chụp màn hình
    image = ImageGrab.grab()
    # Chuyển đổi ảnh sang định dạng numpy array
    image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image_np
hand = []
exactly = 0.75
while True:
   
    img = capture_screen()
    img_resized = cv2.resize(img, (mask.shape[1], mask.shape[0]))
    imgRegion = cv2.bitwise_and(img_resized, mask)
    results = model(imgRegion, stream=True)
   
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100 # độ chính xác
            cls = int(box.cls[0]) # Thứ tự nhận dạng trong classname
            
            if classNames[cls] not in hand and conf > exactly:
                hand.append(classNames[cls])
                print(hand)
                
                #classNames[cls] # tên card
                #cards[classNames[cls]] # Giá trị
                pos_h = cards[classNames[cls]][0]
                pos_w = cards[classNames[cls]][1]
                
                # print(f'{classNames[cls]} - {cards[classNames[cls]]}')
                bg_image[pos_h:pos_h + heightx, pos_w:pos_w + widthx] = card_x
            
            
            
    
    #S -> Bích
    #C -> Chuồng
    #D -> Rô
    #H -> Cơ
 
    cvzone.putTextRect(bg_image, f'Cards:  {52 - len(hand)}', (19, 30), scale=2, thickness=2)
    cvzone.putTextRect(bg_image, f'Exactly:  {int(exactly * 100)}%', (19, 75), scale=2, thickness=2)
    cv2.imshow('List Card', bg_image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        card_positions = {card_name: False for card_name in classNames}
        cv2.imshow('List Card', bg_image)
        
cv2.destroyAllWindows()
    
    
    
    
    

# col1, col2 = st.columns([4,1])
# col1.markdown(" # Well come to my App")
# col2.markdown(" # Well come to my App")
# col1.markdown(" this is column 1")
# uploadPhoto = col2.file_uploader("Tải ảnh lên")
# cameraInput  = col2.camera_input("Chụp ảnh")