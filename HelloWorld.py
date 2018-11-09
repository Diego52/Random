import cv2

cap = cv2.VideoCapture(0)

while True:
    _, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cv2.putText(image, 'HELLO WORLD', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 5)
    cv2.rectangle(image, (60, 60), (100,100), (0, 255, 0), 5)
    image = cv2.resize(image, (1080, 720), interpolation = cv2.INTER_AREA)
    image[200:400, 100:400] = cv2.GaussianBlur(image[200:400, 100:400],(23, 23), 30)
    image2 = image[500:720, 0:1080]
    cv2.imshow('Image', image2)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break