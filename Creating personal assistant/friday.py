from dis import Instruction
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import openai
import dlib
import imutils
import cv2
from imutils import face_utils
from scipy.spatial import distance
from pygame import mixer
from random import randint
import webbrowser
import random

listener = sr.Recognizer()
machine = pyttsx3.init()
openai.api_key = "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"

def talk(text):
    machine.say(text)
    machine.runAndWait()

def listen_instruction():
    instruction = "" 
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = listener.listen(source)
            instruction = listener.recognize_google(audio)
            instruction = instruction.lower()
            if "friday" in instruction:
                instruction = instruction.replace('friday', "")
                print(instruction)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
    return instruction

def generate_chat_response(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()
def drowsiness_detector():
    mixer.init()
    mixer.music.load("music.wav")
    def eye_aspect_ratio(eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    thresh = 0.25
    flag = 0
    frame_check = 20
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['left_eye']
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['right_eye']
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame= imutils.resize(frame ,width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEar = eye_aspect_ratio(leftEye)
            rightEar = eye_aspect_ratio(rightEye)
            ear = (leftEar + rightEar) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            
            if ear < thresh:
                flag += 1
                print(flag)
                if flag >= frame_check:
                    cv2.putText(frame, "***ALERT***", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    mixer.music.play()
            else:
                flag = 0

        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_random_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "I used to play piano by ear, but now I use my hands!",
    ]
    return jokes[randint(0, len(jokes)-1)]

def play_friday():
    instruction = listen_instruction()
    print(instruction)

    if "play" in instruction:
        song = instruction.replace('play', '')
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in instruction:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk("The current time is " + current_time)
        print("Current time: " + current_time)

    elif 'date' in instruction:
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + current_date)
        print("Current date: " + current_date)

    elif 'what is your name' in instruction:
        talk("I am Friday, your personal assistant. How can I assist you?")


    elif "weather" in instruction:
        search_term = instruction.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        talk("Here is what I found for on google")


    elif ("tell me a joke" or "joke") in instruction:
        joke = get_random_joke()
        talk(joke)
        print(joke)

    elif 'open google maps' in instruction:
        talk("Opening Google Maps")
        webbrowser.open("https://www.google.com/maps")    

    elif 'search for' in instruction:
        location = instruction.replace('search for', '').strip()
        search_query = "https://www.google.com/maps/search/" + location.replace(' ', '+')
        talk("Searching for " + location + " on Google Maps")
        webbrowser.open(search_query)
    
    elif 'toss a coin' in instruction:
        coin = random.choice(['Heads', 'Tails'])
        talk("I tossed a coin and it landed on " + coin)
        print("Coin landed on: " + coin)


    elif 'who is' in instruction:
        person = instruction.replace('who is', '')
        info = wikipedia.summary(person, sentences=1)
        print(info)
        talk(info)

    elif 'search' in instruction:
        search_query = instruction.replace('search', '')
        talk("Searching for " + search_query)
        pywhatkit.search(search_query)

    elif 'stop' in instruction or 'exit' in instruction:
        talk("Goodbye!")
        return False

    elif 'drowsy' in instruction or 'drowsiness' in instruction:
        talk("Turning on the drowsiness detection system!")
        print("Turning on the drowsiness detection system!")
        drowsiness_detector()

    else:
        response = generate_chat_response(instruction)
        if response:
            talk(response)
            print(response)
        else:
            talk("I'm sorry, I didn't quite catch that.")
            print("I'm sorry, I didn't quite catch that.")

    return True

while True:
    if not play_friday():
        break




