import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = aa.Recognizer()
machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    global instruction
    try:
        with aa.Microphone() as origin:
            print("listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "friday" in instruction:
                instruction = instruction.replace('friday', "")
                print(instruction)
    except:
        pass
    return instruction

def play_friday():
    instruction = input_instruction()
    print(instruction)
    if "play" in instruction:
        song = instruction.replace('play', '')
        talk("playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in instruction:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk("Current time is " + current_time)
        print("Current time :"+currnet_time)

    elif 'date' in instruction:
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + current_date)
        print("Current date :"+curent_date)

    elif 'how are you' in instruction:
        talk("I'm fine, how about you?")
        print("I'm fine, how about you?")

    elif 'what is your name' in instruction:
        talk("I am Friday, what can I do for you?")

    elif 'who is' in instruction:
        human = instruction.replace('who is', '')
        info = wikipedia.summary(human, 1)
        print(info)
        talk(info)

    else:
        talk('Please repeat the instructions')

play_friday()
