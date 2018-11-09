import cv2
import numpy as np

def find(video_name):
    cap = cv2.VideoCapture(video_name)    
   
    face_cascade = cv2.CascadeClassifier('detectors/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('detectors/haarcascade_eye.xml')
    r = False
    stop = False
    g = -1
    while(True):
        ret, img = cap.read()
        if img is not None:
            if r:
                img = cv2.rotate(img, g)
                print('Rotating 90° ClockWise')
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            s = np.ones(img.shape, dtype='uint8') * 30
            img = cv2.subtract(img, s)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            i = 0

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x , y), (x+w, y+h), (0, 0, 255), 2)
                roi_gray = gray[y:y+h, x:x+w]
                if not stop:
                    roi_color = img[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        i += 1
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            if i < 1 and not stop:
                r = True
                g += 1
                if g > 2:
                    g = 0
            else:
                stop = True
                break
            img = cv2.resize(img, (360, 640), interpolation = cv2.INTER_AREA)
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    
    return r, g