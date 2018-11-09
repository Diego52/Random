import os
import sys
import json
import input_data
import speech_recognition as sr
import pyttsx3
import time
import serial
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '9fb5c901b7924dffb265ede666a00a71'
path = "C:\Developer"
filename = "chatbot"
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
try: 
    ArduinoSerial = serial.Serial('com3',9600)
except:
    print("No serial devices on the selected com")
    pass
def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<chatbot-b4841>"

    if int(choice) == 0:
        print("\n Say something to the Chatbot! \n")
        request.query = input_data.get_value() 
    if int(choice) == 1:
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.adjust_for_ambient_noise(source)
            print("\nSay something!")
            audio = r.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            voice = r.recognize_google(audio)
            print("\nYou said: " +  voice )
            request.query = voice
        except sr.UnknownValueError:
            pass
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("\nCould not request results from Google Speech Recognition service; {0}".format(e))
    response = request.getresponse()
    data = response.read().decode("utf-8")
    data = json.loads(data)
    with open('chatbot.json', 'w') as outfile:
        json.dump(data, outfile)
    
    try:

        data = data['result']['fulfillment']['speech']
    
    except:
        data = "Dont be shy!"
    data2 = "\nChatbot: " + data
    print (data2)
    engine.say(data)
    engine.runAndWait()
    if data == "Good bye!":
        sys.exit() 
    elif data == "Turning on the red light":
        ArduinoSerial.write('0'.encode())
    elif data == "Turning on the blue light":
        ArduinoSerial.write('1'.encode())
    elif data == "Turning off the red light":
        ArduinoSerial.write('2'.encode())
    elif data == "Turning off the blue light":
        ArduinoSerial.write('3'.encode())
    
    



if __name__ == '__main__':
    
    print("\n Choose text or voice \n")
    print("0- Text\n1- Voice")
    choice = input_data.get_value() 
    while True:
        main()