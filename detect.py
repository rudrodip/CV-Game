import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
import math


cap = cv2.VideoCapture(0)
# resize
frameResizeFactor = 0.7

# width and height of video capture
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# warpped width and height
warpWidth = int(width)
warpHeight = int(height)

# selected points and points to transform
selectedPts = np.empty((0, 2), np.float32)
warppedPts = np.empty((0, 2), np.float32)

# if 4 points are selected, then warp should be true
warpTrue = False
# transformation matrix is None at initialization
matrix = None

# color finder
colorFinder = ColorFinder(False)
# hsv value
hsvVals = {"hmin": 139, "smin": 48, "vmin": 134, "hmax": 167, "smax": 255, "vmax": 253}


def getArea(event, x, y, flags, param):
    global selectedPts, warpTrue, warpWidth, warpHeight, matrix

    if event == cv2.EVENT_LBUTTONDOWN and selectedPts.shape[0] <= 4:
        selectedPts = np.append(selectedPts, np.float32([[x, y]]), axis=0)

    if selectedPts.shape[0] >= 4:
        if matrix is None:
            getProportion()
            matrix = cv2.getPerspectiveTransform(selectedPts, warppedPts)
        warpTrue = True
    else:
        warpTrue = False


def drawCircles(pts, frame):
    for pt in pts:
        cv2.circle(frame, (int(pt[0]), int(pt[1])), 2, (0, 255, 0), -1)

def getProportion():
    global warpWidth, warpHeight, warppedPts
    pt1, pt2, pt3 = selectedPts[0], selectedPts[1], selectedPts[2]

    l1 = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
    l2 = math.sqrt((pt2[0] - pt3[0])**2 + (pt2[1] - pt3[1])**2)

    proportion = l1/l2

    warpHeight = int(l2 * 1.5)
    warpWidth = int(warpHeight * proportion)
    warppedPts = np.float32([[0, 0], [warpWidth, 0], [warpWidth, warpHeight], [0, warpHeight]])

    print(proportion)

# main loop
def loop():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # drawCircles where selected points are
        drawCircles(selectedPts, frame)

        if warpTrue:
            frame = cv2.warpPerspective(frame, matrix, (warpWidth, warpHeight))
            frame = cv2.resize(frame, (0, 0), None, frameResizeFactor, frameResizeFactor)

            # color finder
            imageColor, mask = colorFinder.update(frame, hsvVals)
            frame, contours = cvzone.findContours(frame, mask, minArea=200)

            if contours:
                cx, cy = contours[0]["center"]
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # showing frames
        cv2.imshow("Video", frame)

        # mouse event
        cv2.setMouseCallback("Video", getArea)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    loop()