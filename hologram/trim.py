import cv2
import numpy as np
import sys

data = cv2.imread("2.bmp",0)
resize = data[127:127+256, 127:127+256]
cv2.imwrite("2trim.bmp",resize)