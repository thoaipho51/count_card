import cv2
import math
import cvzone



card_x = cv2.imread('Images/X.png')
bg_image = cv2.imread('Images/card_board.png')
mask = cv2.imread('Images/region.png')

# lấy kích thước của ảnh
height, width = 651, 301
heightx, widthx = 52, 32
