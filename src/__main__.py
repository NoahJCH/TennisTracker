import cv2
from src.circle_detection import CircleDetect

cap = cv2.VideoCapture(0)
circleDetector = CircleDetect()

# loop over each frame in video input
while True:
    ret, frame = cap.read()

    # show the output frame
    circleDetector.contour_detect(frame)

    key = cv2.waitKey(1) & 0xFF

    # break when q key is pressed
    if key == ord("q"):
        break

# cleanup windows
cap.release()
cv2.destroyAllWindows()
