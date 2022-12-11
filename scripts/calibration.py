import cv2
import cvzone
from cv2 import aruco
from cvzone.ColorModule import ColorFinder
import numpy as np
import random


class CameraFeed:

    def __init__(self, camera=0, debugger=False):

        self.camera = camera
        # capturing the camera
        self.cap = cv2.VideoCapture(camera)
        self.colorFinder = ColorFinder(debugger) # debugger is disabled
        # hsv value
        self.hsvVals = {'hmin': 31, 'smin': 63, 'vmin': 0, 'hmax': 44, 'smax': 255, 'vmax': 255}
        self.boxes = [[-1, -1], [-1, -1], False]
        self.posList = []


    # function for detecting aruco markers
    def findArucoMarker(self, frame, markerSize=4, posibilities=50, draw=True):
        # converting frame to gray scale
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # getting key for aruco dictionary
        key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{posibilities}')

        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()

        bboxs, ids, rejected = aruco.detectMarkers(grayFrame, arucoDict, parameters=arucoParam)

        if draw:
            aruco.drawDetectedMarkers(frame, bboxs)

        return ids, bboxs

    # mouse event handler
    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param[0] = [x, y]

        elif event == cv2.EVENT_LBUTTONUP:
            param[2] = True

        if not param[2]:
            param[1] = [x, y]


    # drawing rectangle for crop
    def draw_rect(self, boxes, frame):
        start, end, draw = boxes
        if start != [-1, -1]:
            image = cv2.rectangle(frame, (start[0], start[1]), (end[0], end[1]), (0, 255, 0), 1)
            return image
        return frame

    def process_frame(self, frame, frameResizeFactor, column, showContours, showPos):
        self.findArucoMarker(frame)

        if self.boxes[0] != [-1, -1] and not self.boxes[2]:
            self.draw_rect(self.boxes, frame)
                
        if self.boxes[2]:
            crop = frame[self.boxes[0][1]:self.boxes[1][1],self.boxes[0][0]:self.boxes[1][0]]

            imageColor, mask = self.colorFinder.update(crop, self.hsvVals)
            imageContours, contours = cvzone.findContours(
                crop, mask, minArea=200
            )

            if contours and showContours:
                cx, cy = contours[0]["center"]
                area = int(contours[0]["area"])
                cv2.circle(crop, (cx, cy), 5, (0, 255, 0), -1)
                self.posList.append(contours[0]['center'])

                cv2.putText(crop, f'({cx}, {cy}, {area})', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            if showPos:
                for i, pos in enumerate(self.posList):
                    cv2.circle(crop, pos, 5, (0, 255, 0), -1)
                    if i == 0:
                        cv2.line(crop, pos, pos, (255, 0, 0), 2)
                    cv2.line(crop, pos, self.posList[i-1], (255, 0, 0), 2)

            frame = cvzone.stackImages([crop, imageContours, imageColor, mask], column, frameResizeFactor)

        return frame


    # main function for getting all frames
    def getFrames(self, frameResizeFactor=0.4, column=2, showPos=False, showContours=True):
        self.boxes = [[-1, -1], [-1, -1], False]

        while True:
            success, frame = self.cap.read()
            
            if not success: break

            imgStack = self.process_frame(frame, frameResizeFactor, column, showContours, showPos) 
            cv2.imshow('Stack', imgStack)

            if not self.boxes[2]:
                cv2.imshow('video', frame)
                cv2.setMouseCallback('video', self.on_mouse, param=self.boxes)


            key = cv2.waitKey(20)
            if key == ord('q'):
                break
            if key == ord(' '):
                cv2.waitKey(-1)
            if key == ord('c'):
                cv2.imwrite(f'saved/{random.randint(0, 1000)}.png', frame)

            # checks if the window 'video' exist, if and self.boxes[0] -> {this boolean variables gives where specific points are given to crop the image} then destroy the window
            if cv2.getWindowProperty('video', cv2.WND_PROP_VISIBLE) >= 1 and self.boxes[2]:
                cv2.destroyWindow('video')

        # When everything is done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = CameraFeed(camera='test_example.mp4', debugger=False)
    cam.getFrames(frameResizeFactor=0.6, showPos=True) 