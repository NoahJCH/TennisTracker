import cv2
import imutils
import numpy as np

from src.speedgraph import SpeedGraph


# utility function for distance between two points
def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def speed_to_text(speed):
    return str(np.floor(speed * 10) / 10) + "km/h"


# filters the frame to only potential tennis ball colors
def color_restrict(frame):
    # lower bound and upper bound for Green color

    # using BGR bound filtering
    lower_bound = np.array([30, 95, 75])
    upper_bound = np.array([235, 255, 255])
    # find the colors within the boundaries
    mask = cv2.inRange(frame, lower_bound, upper_bound)
    frame = cv2.bitwise_and(frame, frame, mask=mask)

    # repeat for hsv bounds
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([25, 10, 50])
    upper_bound = np.array([95, 150, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # clean up the mask pixels
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    frame = cv2.bitwise_and(frame, frame, mask=mask)
    return frame


class CircleDetect:
    tennisBallSize = 66  # radius in mm
    frameRate = 30  # camera frames per second

    # variables storing the previous data for the different algorithms
    blobPrevCircles = []
    prevCircle = None
    prevPoint = []

    maxSpeed = 0
    speedGraph = SpeedGraph()

    # display a frame, its speed, and its speed graph
    def display(self, frame, speed):
        frame = cv2.flip(frame, 1)

        # text parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (25, 25)
        font_scale = 1
        color = (0, 255, 255)
        thickness = 2

        # write the text to the frame
        frame = cv2.putText(frame, speed_to_text(speed) + ", max: " + speed_to_text(self.maxSpeed), org, font,
                            font_scale, color, thickness, cv2.LINE_AA)

        # display frame
        cv2.imshow("Speed Graph", self.speedGraph.graph(speed))
        cv2.imshow("Tennis Tracker", frame)

    def contour_detect(self, frame):
        if frame is None:
            return

        # pre-process the frame to only tennis ball colours
        blur_frame = cv2.GaussianBlur(frame, (13, 13), 0)
        hsv = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)

        lower_bound = np.array([25, 40, 20])
        upper_bound = np.array([95, 170, 215])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the frame
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        scale = None

        if len(cnts) > 0:
            # choose the contour with the largest area
            chosen = max(cnts, key=cv2.contourArea)

            # get the coordinates of the chosen contour
            ((x, y), radius) = cv2.minEnclosingCircle(chosen)
            M = cv2.moments(chosen)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # display a circular outline on the chosen contour
            # and update the tail - line
            if radius > 10:
                self.prevPoint.append(center)
                scale = radius
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)

        line = self.prevPoint

        #calculate speed
        speed_kph = 0
        if len(line) > 3 and scale is not None:
            p1 = line[-4]
            p2 = line[-1]
            travel_dist = dist(p2[0], p2[1], p1[0], p1[1])
            speed = travel_dist * self.tennisBallSize * (self.frameRate / 3) / scale  # mm/s
            speed_kph = speed * 3.6 / 1000 # convert to km/h

        # draw the line
        for i in range(len(line) - 1):
            cv2.line(frame, line[i], line[i + 1], (0, 255, 255), 10)

        if len(line) > 10:
            self.prevPoint.pop(0)

        self.maxSpeed = max(speed_kph, self.maxSpeed)

        self.display(frame, speed_kph)

