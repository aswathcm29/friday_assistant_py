from dis import Instruction
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

def listen_instruction():
    instruction = "" # Initialize with a default value
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

def play_friday():
    instruction = listen_instruction()
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
        talk("I am Friday, your personal assistant. How can I assist you?")

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

    else:
        # Generate response using ChatGPT
        response = generate_chat_response(instruction)
        talk(response)
        print(response)

    return True

while True:
    if not play_friday():
        break











