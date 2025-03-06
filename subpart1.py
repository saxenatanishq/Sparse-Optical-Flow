import cv2 as cv
import numpy as np
import lukas

cap = cv.VideoCapture("OPTICAL_FLOW.mp4")
feature_params = dict(maxCorners = 300, qualityLevel = 0.2, minDistance = 7, blockSize = 3)
lk_params = dict(winsize = 9, maxLevel = 2, epsilon_lower = 0.01, epsilon_higher = 1000, max_count = 2, fps = cap.get(cv.CAP_PROP_FPS))
color_line = (0,255,0)
color_corner = (0,0,255)
ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
mask = np.zeros_like(first_frame)

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
    next_points = lukas.LK(prev_gray, gray, prev, **lk_params)
    good_old = prev.astype(int)
    good_new = next_points.astype(int)
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv.line(mask, (a, b), (c, d), color_line, 3)
        frame = cv.circle(frame, (a, b), 3,color_corner, -1)
    output = cv.add(frame, mask)
    prev_gray = gray.copy()
    cv.imshow("sparse optical flow", output)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()