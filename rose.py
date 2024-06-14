# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2

src = cv2.imread('rose.bmp')

if src is None:
    print('failed to load image!')
    sys.exit()


src_ycrcb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)

#Y 채널만을 float32 형태로 추출합니다.
src_f = src_ycrcb[:, :, 0].astype(np.float32)


blr = cv2.GaussianBlur(src_f, (0, 0), 2.0)

# 원본 Y 채널과 블러 적용된 이미지의 차이를 이용하여 이미지의 선명도를 높입니다.
src_ycrcb[:, :, 0] = np.clip(2. * src_f - blr, 0, 255).astype(np.uint8)

# YCrCb 색공간에서 BGR 색공간으로 다시 변환합니다.
dst = cv2.cvtColor(src_ycrcb, cv2.COLOR_YCrCb2BGR)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()

cv2.destroyAllWindows()
