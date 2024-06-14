import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

src = cv2.imread('Hawkes.jpg', cv2.IMREAD_GRAYSCALE)

if src is None:
    print('Image Load Failed')
    sys.exit()
alpha = 1.0
dst = cv2.normalize(src, None, 0, 255, cv2.NORM_MINMAX)
hist_src = cv2.calcHist([src], [0], None, [256], [0, 256])
hist_dst = cv2.calcHist([dst], [0], None, [256], [0, 256])
cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()
plt.plot(hist_src)
plt.plot(hist_dst)
plt.show()
