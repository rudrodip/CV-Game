import cv2
from cv2 import aruco


def generateArucoMarker(filename, marker_size, possibilities, image_size, id):
    key = getattr(aruco, f"DICT_{marker_size}X{marker_size}_{possibilities}")
    arucoDict = aruco.Dictionary_get(key)
    marker_image = aruco.drawMarker(arucoDict, id, image_size)
    cv2.imwrite(filename, marker_image)

    print(f"ArUco marker with id {id} size {marker_size} created at {filename}")


for i in range(4):
    generateArucoMarker(
        f"marker_{i}.png",
        marker_size=4,
        possibilities=50,
        image_size=200,
        id=i,
    )
