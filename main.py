import math
import random
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone


# "IP:PORT/video For Ip webcam


# Initialize the webcam
cap = cv2.VideoCapture('http://192.0.0.4:8080/video',cv2.CAP_FFMPEG)  # Change the index as needed

# cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Width set for 480p
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Height set for 480p

# Initialize the hand detector
detector = HandDetector(detectionCon=0.4, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []  # Snake points
        self.lengths = []  # Distance between points
        self.currentLength = 0  # Total length
        self.allowedLength = 150  # Max length
        self.previousHead = (0, 0)  # Previous head position

        # Load and set the food
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = (0, 0)
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = (random.randint(100, 540), random.randint(100, 380))

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [200, 250], scale=5, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [200, 350], scale=5, thickness=5, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append((cx, cy))
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = (cx, cy)

            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1

            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)

            pts = np.array(self.points[:-2], np.int32).reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1:
                self.gameOver = True
                self.reset()

        return imgMain

    def reset(self):
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = 150
        self.previousHead = (0, 0)
        self.randomFoodLocation()
        self.score = 0

game = SnakeGameClass("donut.png")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game.reset()
    if key == 32:  # 32 is the ASCII code for the space bar
        break  # Exit the loop
