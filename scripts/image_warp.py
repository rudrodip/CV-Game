import cv2
import numpy as np
import math
import random
import cvzone
from cv2 import aruco
from cvzone.ColorModule import ColorFinder

class ImageWarp:
    def __init__(self):
        # selected points and points to transform
        self.selectedPts = np.empty((0, 2), np.float32)
        self.warppedPts = np.empty((0, 2), np.float32)

        self.warpped = False
        self.matrix = None

        self.colorFinder = ColorFinder(False) # debugger is disabled
        # hsv value
        self.hsvVals = {'hmin': 31, 'smin': 63, 'vmin': 0, 'hmax': 44, 'smax': 255, 'vmax': 255}

    def setProportion(self):
        pt1, pt2, pt3 = self.selectedPts[:3]

        dis = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)

        l1 = dis(pt1[0], pt1[1], pt2[0], pt2[1])
        l2 = dis(pt2[0], pt2[1], pt3[0], pt3[1])

        proportion = l1 / l2 # width/height

        self.warpHeight = int(l2 * 1.5)
        self.warpWidth = int(self.warpHeight * proportion)

        self.warppedPts = np.float32(
            [[0, 0], [self.warpWidth, 0], [self.warpWidth, self.warpHeight], [0, self.warpHeight]]
        )

    def warppedImage(self, frame):
        warppedFrame = cv2.warpPerspective(
                        frame, self.matrix, (self.warpWidth, self.warpHeight)
                    )
        return warppedFrame



class LiveWarp(ImageWarp):

    def __init__(self, cameraType='video', source=0):
        super().__init__()
        self.cameraType = cameraType
        self.source = source

        if cameraType == 'video':
            self.cap = cv2.VideoCapture(source)


    def setPoints(self, event, x, y, flags, params):
        x, y = int(x), int(y)
        if event == cv2.EVENT_LBUTTONDOWN and self.selectedPts.shape[0] <= 4:
            self.selectedPts = np.append(self.selectedPts, np.float32([[x, y]]), axis=0)

        if self.selectedPts.shape[0] >= 4:
            if self.matrix is None:
                self.setProportion()
                self.matrix = cv2.getPerspectiveTransform(self.selectedPts, self.warppedPts)
            self.warpped = True
        else:
            self.warpped = False

    def drawCircles(self, pts, frame):
        for pt in pts[:4]:
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 2, (0, 255, 0), -1)

    def frameProcessing(self, frame, resizeFactor):
        if self.warpped:
            frame = self.warppedImage(frame)
        else:
            self.drawCircles(self.selectedPts, frame)

        # imageColor, mask = self.colorFinder.update(frame, self.hsvVals)
        # imageContours, contours = cvzone.findContours(
        #     frame, mask, minArea=200
        # )

        # if contours:
        #     cx, cy = contours[0]["center"]
        #     area = int(contours[0]["area"])
        #     cv2.circle(imageContours, (cx, cy), 5, (0, 255, 0), -1)
        #     cv2.putText(imageContours, f'({area})', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        frame = cv2.resize(frame, (0, 0), None, resizeFactor, resizeFactor)
        return frame


    def frameLoop(self, windowName='video', resizeFactor=1):
        while True:
            if self.cameraType == 'video':
                success, frame = self.cap.read()
            else:
                success, frame = True, cv2.imread(self.source)
            
            if not success:
                break
            else:
                frame = self.frameProcessing(frame, resizeFactor)
                cv2.imshow(windowName, frame)

            # mouse event
            cv2.setMouseCallback(windowName, self.setPoints)

            key = cv2.waitKey(20)
            if key == ord('q'):
                break
            if key == ord(' '):
                cv2.waitKey(-1)
            if key == ord('c'):
                cv2.imwrite(f'saved/save{random.randint(0, 100)}.png', frame)

        # When everything is done, release the capture
        if self.cameraType == 'video':
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = LiveWarp(cameraType='video', source=0)
    cam.frameLoop(windowName='video warp', resizeFactor=1)