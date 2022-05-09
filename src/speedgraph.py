import cv2
import numpy as np

# define constants
height = 480
width = 640
maxSpeedListLen = 30 * 8


class SpeedGraph:
    # speedList stores the calculated speeds from the last 8 seconds
    speedList = []

    # this returns the max speed from speedList
    def max_speed(self):
        return max(self.speedList)

    # returns the (x, y) point in the graph for a speed value
    def speed_to_pt(self, speed, index):
        return int(width * (index / maxSpeedListLen)), int(height * (speed / self.max_speed()))

    # updates graph with new speed and returns the frame
    def graph(self, speed):
        frame = np.zeros(shape=[height, width, 3], dtype=np.uint8)  # blank frame
        self.speedList.append(speed)

        if len(self.speedList) > maxSpeedListLen:
            self.speedList.pop(0)

        # graph the speeds
        line = self.speedList
        for i in range(len(line) - 1):
            if self.max_speed() == 0:
                break
            location1 = self.speed_to_pt(line[i], i)
            location2 = self.speed_to_pt(line[i + 1], i + 1)
            frame = cv2.line(frame, location1, location2, (0, 255, 255), 4)

        for i, pt in enumerate(self.speedList):
            if self.max_speed() == 0:
                break
            location = (int(width * ( i / maxSpeedListLen)), int(height * (pt / self.max_speed())))
            frame = cv2.circle(frame, location, 0, (0, 0, 255), -1)

        frame = cv2.flip(frame, 0)
        return frame
