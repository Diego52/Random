import cv2
import threading
import os, sys, inspect, thread, time
import paho.mqtt.publish as publish
import pyttsx3
import datetime
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = 'LeapDeveloper/LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapDeveloper/LeapSDK//lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, ScreenTapGesture

data = {
    'Gesture': None,
    'finger_names' : ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'],
    'Clock': None
}
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print ("Connected")
        # Enable gestures     
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                data['Gesture'] = 'circle'
                print('SCANNING')
                circle = CircleGesture(gesture)
                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    data['Clock'] = "clockwise"
                else:
                    data['Clock'] = "counterclockwise"
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                publish.single("homewatchtest-door", 'hola', hostname="test.mosquitto.org")
                print('OPENING DOOR')
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                now = datetime.datetime.now()
                print(str(now))
                data2 = "Current year: %d" % now.year + "              ,Current month: %d" % now.month + "         ,Current day: %d" % now.day
                engine.say(data2)
                engine.runAndWait()

                
def Motion():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
    return(data)

class ThreadingEvaluation(object):

    def __init__(self, interval=1):
        self.interval = interval

        thread2 = threading.Thread(target=self.run, args=())
        thread2.daemon = True                            # Daemonize thread
        thread2.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        Motion()


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
        if data['Gesture'] == 'circle' and data['Clock'] == 'clockwise':
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
                    i += int((h/20))
                else:
                    i = i - int((h/20))
                if i >= h:
                    op = 1
                elif i <= 0:
                    op = 0
                cv2.line(image, (x, y + i), (x + w, y + i), (0, 255, 0), 2)


        image = cv2.resize(image, (360, 640), interpolation = cv2.INTER_AREA)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    evaluation = ThreadingEvaluation()
    webcam_face_recognizer()
    