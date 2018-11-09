import cv2

cap =  cv2.VideoCapture(1)

while True: 
    _, img = cap.read()
    cv2.imshow('frame',img)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()