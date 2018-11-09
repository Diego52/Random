from Faces import webcam_face_recognizer
import serial
import pyttsx3
import sys
import time
try: 
    ArduinoSerial = serial.Serial('com5',9600)
except:
    print("No serial devices on the selected com")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
        


if __name__ == "__main__":
    Start = webcam_face_recognizer()
    ArduinoSerial.write('3'.encode()) 
    while True:
        myData = None
        if (ArduinoSerial.inWaiting()>0):
            myData = ArduinoSerial.readline()
            myData = myData.decode("utf-8")
            myData = myData.rstrip()
            myData = int(myData)
            print(myData)
            if(myData == 0):
                data = "You are at the office one"
                engine.say(data)
                engine.runAndWait()
            elif (myData == 1):
                data = "You are at the office two"
                engine.say(data)
                engine.runAndWait()
            
            elif (myData == 2):
                data = "You are at the office three"
                engine.say(data)
                engine.runAndWait()
            else:
                continue
    
    
                    



