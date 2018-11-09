import cv2

def webcam_face_recognizer():
    print('\n*************************')
    print('Face Recognition System')
    print('*************************\n')
    face_cascade = cv2.CascadeClassifier('frecogn/detectors/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    i  = 0
    op = 0
    while True: 
        _, image = cap.read() 
        pic = image
        pic = cv2.resize(pic, (400,300))
        list_faces = list()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            dict_face = dict()
            faceAligned = image[y:y+h,x:x+w]
            dict_face['coords'] = (x, y, w, h)
            dict_face['image'] = faceAligned
            list_faces.append(dict_face)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, 'BEAUTIFUL', (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)                    
            image[y:y+h, x:x+w] = cv2.GaussianBlur(image[y:y+h, x:x+w],(23, 23), 30)
            if op == 0:
                i += int((h/50))
            else:
                i = i - int((h/50))
            if i >= h:
                op = 1
            elif i <= 0:
                op = 0
            cv2.line(image, (x, y + i), (x + w, y + i), (0, 255, 0), 2)
            image = cv2.resize(image, (360, 640), interpolation = cv2.INTER_AREA)
            cv2.imshow('frame', image)
            cv2.waitKey(1)


        image = cv2.resize(image, (360, 640), interpolation = cv2.INTER_AREA)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    webcam_face_recognizer()
    