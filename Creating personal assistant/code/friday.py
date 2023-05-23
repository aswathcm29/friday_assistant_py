import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import openai

listener = sr.Recognizer()
machine = pyttsx3.init()
openai.api_key = "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"

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    instruction = ""  # Initialize with a default value
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = listener.listen(source)
            instruction = listener.recognize_google(audio)
            instruction = instruction.lower()
            if "friday" in instruction:
                instruction = instruction.replace('friday', "")
                print(instruction)
    except:
        pass
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

def play_friday():
    instruction = input_instruction()
    print(instruction)

    if "play" in instruction:
        song = instruction.replace('play', '')
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in instruction:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk("Current time is " + current_time)
        print("Current time: " + current_time)

    elif 'date' in instruction:
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + current_date)
        print("Current date: " + current_date)


    elif 'what is your name' in instruction:
        talk("I am Friday, what can I do for you?")

    elif 'who is' in instruction:
        human = instruction.replace('who is', '')
        info = wikipedia.summary(human, 1)
        print(info)
        talk(info)

    else:
        # Generate response using ChatGPT
        response = generate_chat_response(instruction)
        talk(response)
        print(response)

play_friday()
