import sys #시험 추가로 객체가 바뀔 수 있는지 첫번째 코딩 문제!!!
import numpy as np
import cv2


# ?엯?젰 ?씠誘몄?? 遺덈윭?삤湲?
src = cv2.imread('coins1.jpg')

if src is None:
    print('Image open failed!')
    sys.exit()

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
blr = cv2.GaussianBlur(gray, (0, 0), 1)

# ?뿀?봽 蹂??솚 ?썝 寃?異?
circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 50,
                           param1=150, param2=40, minRadius=20, maxRadius=80)
#블러처리 이미지, 허프변환 알고리즘, 픽셀해상도, 하프변환배열 누적크기, 내부사용값, 원검출 임계값, 검출 원 반지름 최소, 검출 원 반지름 최대

# ?썝 寃?異? 寃곌낵 諛? ?룞?쟾 湲덉븸 異쒕젰
sum_of_money = 0
dst = src.copy()
if circles is not None:
    for i in range(circles.shape[1]):
        cx, cy, radius = np.uint16(circles[0][i]) 
        #원의 중심좌표와 반지름 정수형 반환한다. i번째 원을 추출한다. i번째 원의 반지름 중심좌표를 배열에 담는다.
        cv2.circle(dst, (cx, cy), radius, (0, 0, 255), 2, cv2.LINE_AA)

        # 원의 영역을 추출한다. 
        #cx에서 반지름을 뺀 원의 왼쪽 경계 x좌표, 검출된 원 좌표를 잘라낼 영역의 좌표, cx에서 반지름을 더한 원의 오른쪽 경계 x좌표
        x1 = int(cx - radius)
        y1 = int(cy - radius)
        x2 = int(cx + radius)
        y2 = int(cy + radius)
        radius = int(radius)
        
        crop = dst[y1:y2, x1:x2, :] #검출된 영역을 추출한다. (y1, y2) 범위, (x1,x2)범위의 열 추출
        ch, cw = crop.shape[:2] #잘라낸 부분 이미지 crop 높이 ch와 cw 너비

        # 원 내부영역 마스크 생성 
        mask = np.zeros((ch, cw), np.uint8)
        cv2.circle(mask, (cw//2, ch//2), radius, 255, -1)

        # 원 내부의 hue 평균값 생성. hue 색 성분 +40, shift하고 평균을 계산한다. 
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV) #추출된 영역을 hsv로 반환한다.
        hue, _, _ = cv2.split(hsv) #hue 채널 분리
        hue_shift = (hue + 40) % 180 #hue 값을 40만큼 이동시킨뒤 평균 계산하는 방법
        mean_of_hue = cv2.mean(hue_shift, mask)[0]

        # Hue 평균이 90보다 작으면 10원 그렇지 않으면 100원 
        won = 100
        if mean_of_hue < 90:
            won = 10

        sum_of_money += won

        cv2.putText(crop, str(won), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (255, 0, 0), 2, cv2.LINE_AA)

cv2.putText(dst, str(sum_of_money) + ' won', (40, 80),
            cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()

cv2.destroyAllWindows()
