import cv2
import cvzone
import cv2.aruco as aruco
from cvzone.ColorModule import ColorFinder
import numpy as np
import math


class CameraFeed:

    def __init__(self, frameResizeFactor=0.7, videoFormat="warpped", showContours=True, camera=0):

        # setting initial variables
        self.frameResizeFactor = frameResizeFactor
        self.videoFormat = videoFormat
        self.showContours = showContours
        self.camera = camera

        # capturing the camera
        self.cap = cv2.VideoCapture(camera)

        # width and height of video capture
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # warpped width and height
        self.warpWidth = int(self.width)
        self.warpHeight = int(self.height)

        # selected points and points to transform
        self.selectedPts = np.empty((0, 2), np.float32)
        self.warppedPts = np.empty((0, 2), np.float32)

        self.warpped = False
        self.matrix = None

        self.colorFinder = ColorFinder(False) # debugger is disabled
        # hsv value
        self.hsvVals = {"hmin": 139, "smin": 48, "vmin": 134, "hmax": 167, "smax": 255, "vmax": 253}


    def findArucoMarker(self, frame, markerSize=6, posibilities=250, draw=True):
        # converting frame to gray scale
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # getting key for aruco dictionary
        key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{posibilities}')

        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()

        bboxs, ids, rejected = aruco.detectMarkers(grayFrame, arucoDict, parameters=arucoParam)

        if draw:
            aruco.drawDetectedMarkers(frame, bboxs)


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

    def getFrames(self):
        while True:
            success, frame = self.cap.read()
            warppedFrame = frame

            if not success:
                break
            else:
                self.drawCircles(self.selectedPts, frame)

                if self.warpped:
                    warppedFrame = cv2.warpPerspective(
                        frame, self.matrix, (self.warpWidth, self.warpHeight)
                    )
                    warppedFrame = cv2.resize(
                        warppedFrame, (0, 0), None, self.frameResizeFactor, self.frameResizeFactor
                    )

                    # color finder
                    imageColor, mask = self.colorFinder.update(warppedFrame, self.hsvVals)
                    warppedFrame, contours = cvzone.findContours(
                        warppedFrame, mask, minArea=200
                    )

                    if contours and self.showContours:
                        cx, cy = contours[0]["center"]
                        cv2.circle(warppedFrame, (cx, cy), 5, (0, 255, 0), -1)

                    self.findArucoMarker(warppedFrame)

            if self.videoFormat == "raw":
                cv2.imshow("Video", frame)
            elif self.videoFormat == "warpped":
                cv2.imshow("Video", warppedFrame)
            elif self.videoFormat == "imgColor":
                cv2.imshow("Video", imageColor)
            elif self.videoFormat == "mask":
                cv2.imshow("Video", mask)

            # mouse event
            cv2.setMouseCallback("Video", self.setPoints)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # When everything is done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = CameraFeed()
    cam.getFrames()