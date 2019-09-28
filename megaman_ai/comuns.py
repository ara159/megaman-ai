import cv2

sttinf = "\033[;1m\033[1;31m*\033[0;0m"
sttwrn = "\033[;1m\033[1;93m!\033[0;0m"

def mm_resize(frame):
    for s in (0.5, 0.5, 0.75):
        frame = cv2.resize(frame, None, fx=s, fy=s, interpolation=cv2.INTER_BITS)
    frame[frame <= 40] = 0
    return frame