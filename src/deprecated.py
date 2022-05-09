# # deprecated function
#     def blobDetect(self, frame):
#         blurFrame = cv2.GaussianBlur(frame, (17, 17), 0)
#
#         # only yellow/green objects
#         restrictFrame = color_restrict(blurFrame)
#
#         params = cv2.SimpleBlobDetector_Params()
#
#         # Set Area filtering parameters
#         params.filterByArea = True
#         params.minArea = 1000
#         params.maxArea = 10000000
#
#         # Set colour filtering parameters
#         params.filterByColor = True
#         params.blobColor = 255
#
#         # Set Circularity filtering parameters
#         params.filterByCircularity = False
#         params.minCircularity = 0.9
#
#         # Set Convexity filtering parameters
#         params.filterByConvexity = False
#         params.minConvexity = 0.85
#
#         # Set Inertia filtering parameters
#         params.filterByInertia = True
#         params.minInertiaRatio = 0.5
#
#         # Create a detector with the parameters
#         detector = cv2.SimpleBlobDetector_create(params)
#
#         # Detect blobs
#         keypoints = detector.detect(restrictFrame)
#
#         # Draw blobs on our image as red circles
#         blank = np.zeros((1, 1))
#
#         # cv2.bitwise_and(frame, frame, mask=mask)
#
#         # blobs = cv2.drawKeypoints(frame, keypoints, blank, (0, 0, 255),
#         #                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#         #
#         # number_of_blobs = len(keypoints)
#         # text = "Number of Circular Blobs: " + str(number_of_blobs)
#         # cv2.putText(blobs, text, (20, 550),
#         #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
#         # print(text)
#
#         blobs = frame
#
#         if keypoints is not None and len(keypoints) > 0:
#             chosen = None
#             scale = None
#             for point in keypoints:
#                 pt = (int(point.pt[0]), int(point.pt[1]))
#                 if chosen is None:
#                     chosen = pt
#                     scale = point.size
#                 if len(self.blobPrevCircles) > 0:
#                     prev = self.blobPrevCircles[-1]
#                     if dist(chosen[0], chosen[1], prev[0], prev[1]) >= dist(pt[0], pt[1], prev[0], prev[1]):
#                         chosen = pt
#                         scale = point.size
#
#             # calculate speed
#             # speed = 0
#             # if len(self.blobPrevCircles) > 0:
#             #     prev = self.blobPrevCircles[-1]
#             #     if prev != (0, 0):
#             #         travelDist = dist(chosen[0], chosen[1], prev[0], prev[1])
#             #         speed = travelDist * self.tennisBallSize * self.frameRate / scale  # mm / s
#             #         print("speed: " + str(speed))
#             #
#             # if speed < 10000:
#             #     # only add if our speed is appropriate
#             #     blobs = cv2.drawKeypoints(blobs, [cv2.KeyPoint(chosen[0], chosen[1], scale)], blank, (0, 0, 255),
#             #                               cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#             #     self.blobPrevCircles.append(chosen)
#             # else:
#             #     self.blobPrevCircles.append((0, 0))
#
#                 blobs = cv2.drawKeypoints(blobs, [cv2.KeyPoint(chosen[0], chosen[1], scale)], blank, (0, 0, 255),
#                                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#                 self.blobPrevCircles.append(chosen)
#
#             # find path
#             line = self.blobPrevCircles
#             try:
#                 while True:
#                     line.remove((0, 0))
#             except ValueError:
#                 pass
#
#             # if we have a lot of bad values, reset storedCircles.
#             if len(line) == 0 or len(line) + 3 <= len(self.blobPrevCircles):
#                 self.blobPrevCircles = []
#
#             for i in range(len(line) - 1):
#                 cv2.line(blobs, line[i], line[i + 1], (0, 255, 255), 10)
#         # else:
#         #     self.blobPrevCircles.append((0, 0))
#
#         # print(self.blobPrevCircles)
#         if len(self.blobPrevCircles) > 10:
#             self.blobPrevCircles.pop(0)
#
#         # problem - we dont want to include bad data,
#         # but initially all data is bad...
#         # what if we start with empty, and only check for bad data when full.
#         # idk...
#
#         return blobs
#
#     # deprecated function
#     def blobDetectTwo(self, frame):
#         blurFrame = cv2.GaussianBlur(frame, (17, 17), 0)
#
#         params = cv2.SimpleBlobDetector_Params()
#
#         # Set Area filtering parameters
#         params.filterByArea = True
#         params.minArea = 1000
#         params.maxArea = 10000000
#
#         # Set colour filtering parameters
#         params.filterByColor = True
#         params.blobColor = 255
#
#         # Set Circularity filtering parameters
#         params.filterByCircularity = False
#         params.minCircularity = 0.5
#
#         # Set Convexity filtering parameters
#         params.filterByConvexity = False
#         params.minConvexity = 0.85
#
#         # Set Intertia filtering parameters
#         params.filterByInertia = False
#         params.minInertiaRatio = 0.5
#
#         # Create a detector with the parameters
#         detector = cv2.SimpleBlobDetector_create(params)
#
#         # Detect blobs
#         keypoints = detector.detect(blurFrame)
#
#         # Draw blobs on our image as red circles
#         blank = np.zeros((1, 1))
#         blobs = frame
#
#         if keypoints is not None and len(keypoints) > 0:
#             # print(len(keypoints))
#             chosen = None
#             scale = None
#             for point in keypoints:
#                 pt = (int(point.pt[0]), int(point.pt[1]))
#                 scale = point.size
#                 blobs = cv2.drawKeypoints(blobs, [cv2.KeyPoint(pt[0], pt[1], scale)], blank, (0, 0, 255),
#                                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#             self.blobPrevCircles.append(chosen)
#
#         # # find path
#         # line = self.blobPrevCircles
#         # try:
#         #     while True:
#         #         line.remove((0, 0))
#         # except ValueError:
#         #     pass
#         #
#         # for i in range(len(line) - 1):
#         #     cv2.line(blobs, line[i], line[i + 1], (0, 255, 255), 10)
#
#         # print(self.blobPrevCircles)
#         if len(self.blobPrevCircles) > 10:
#             self.blobPrevCircles.pop(0)
#
#         # problem - we dont want to include bad data,
#         # but initially all data is bad...
#         # what if we start with empty, and only check for bad data when full.
#         # idk...
#
#         return blobs
#
#     # deprecated function
#     def houghDetect(self, frame):
#         grayFrame = cv2.cvtColor(color_restrict(frame), cv2.COLOR_BGR2GRAY)
#         blurFrame = cv2.medianBlur(grayFrame, 5)
#
#         rows = blurFrame.shape[0]
#         circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, rows / 8,
#                                    param1=100, param2=30, minRadius=50, maxRadius=400)
#
#         # if circles is not None:
#         #     circles = np.uint16(np.around(circles))
#         #     for circle in circles:
#         #         cv2.circle(frame, (circle[0], circle[1]), 1, (0, 100, 100), 3)
#         #         cv2.circle(frame, (circle[0], circle[1]), circle[2], (255, 0, 255), 3)
#
#         # if circles is not None:
#         #     circles = np.uint16(np.around(circles))
#         #     chosen = None
#         #     for i in circles[0, :]:
#         #         if chosen is None: chosen = i
#         #         if self.prevCircle is not None:
#         #             if dist(chosen[0], chosen[1], self.prevCircle[0], self.prevCircle[1]) <= dist(i[0], i[1],
#         #                                                                                           self.prevCircle[0],
#         #                                                                                           self.prevCircle[1]):
#         #                 chosen = i
#         #     cv2.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
#         #     cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
#         #     self.prevCircle = chosen
#         return frame