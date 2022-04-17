import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def getLineCoordinates(frame, lines):
    slope, yIntercept = lines[0], lines[1]

    # get y and x coordinates

    y1 = frame.shape[0]
    y2 = int(y1 - 250)

    x1 = int((y1 - yIntercept) / slope)

    x2 = int((y2 - yIntercept) / slope)

    return np.array([x1, y1, x2, y2])

    # average out lines from hough transformation


def getLines(frame, lines):
    copyImage = frame.copy()
    leftLine, rightLine = [], []
    lineFrame = np.zeros_like(frame)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # calculate slope & y intercept
        lineData = np.polyfit((x1, x2), (y1, y2), 1)
        slope, yIntercept = round(lineData[0], 1), lineData[1]
        if slope < 0:
            leftLine.append((slope, yIntercept))
        else:
            rightLine.append((slope, yIntercept))

    if leftLine:
        leftLineAverage = np.average(leftLine, axis=0)
        left = getLineCoordinates(frame, leftLineAverage)
        try:
            cv2.line(lineFrame, (left[0], left[1]), (left[2], left[3]), (255, 0, 0), 2)
        except Exception as e:
            print('Error', e)
    if rightLine:
        rightLineAverage = np.average(rightLine, axis=0)
        right = getLineCoordinates(frame, rightLineAverage)
        try:
            cv2.line(lineFrame, (right[0], right[1]), (right[2], right[3]), (255, 0, 0), 2)
        except Exception as e:
            print('Error:', e)

    return cv2.addWeighted(copyImage, 0.8, lineFrame, 0.8, 0.0)



fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 360))

vid = cv2.VideoCapture('lane_vgt.mp4')
count = 0
while (vid.isOpened()):
    ret, frame = vid.read()
    cv2.imshow("original frame", frame)

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img = cv2.medianBlur(img, 5)
    ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    image = cv2.GaussianBlur(th1, (3, 3), 0)
    stencil = np.zeros_like(image)
    polygon = np.array([[0, 300], [150, 240], [280, 100], [580, 380]])
    cv2.fillConvexPoly(stencil, polygon, 1)
    masked_image = cv2.bitwise_and(img, img, mask=stencil)
    thresh_mask = cv2.medianBlur(masked_image, 5)
    ret2, masked = cv2.threshold(masked_image, 127, 255, cv2.THRESH_BINARY)
    masked = cv2.GaussianBlur(masked, (3, 3), 0)
    lines = cv2.HoughLinesP(masked, 1, np.pi / 180, 30, maxLineGap=200)
    imageWithLines = getLines(frame, lines)
    cv2.imshow('final', imageWithLines)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

vid.release()
out.release()
cv2.destroyAllWindows()

