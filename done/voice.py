import importlib
import speech_recognition as sr
import pyttsx3
import time
from threading import Thread
import randomquestionfull



recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 120)  # Giảm tốc độ nói của máy

questions = []
new = randomquestionfull.main()
questions.extend(new)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=4):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""

def countdown(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)
    return True

def part1():
    speak("This is the simulated speaking test and I'm your examiner. Can you hear my voice,   OK please make sure that your microphone is on and keep your surrounding area silent. You should adjust the volume before the test. Are you ready?     OK LET START")
    speak("Now, in this first part, I'd like to ask you some questions about yourself")
    start_time = time.time()
    for question in questions[:10]:
        if time.time() - start_time > 300:  # 5 phút
            break
        speak(question)
        while True:
            response = listen()
            if not response:
                break
    speak("that is the end of part 1, now we will turn to part 2 ")

def part2():
    speak("In part 2, I'm going to give you a topic and I'd like you to talk about it for one to two minutes. Before you talk, you'll have one minute to think about what you are going to say. You can make some notes if you wish. Here's some paper and a pencil for making notes, and here's your topic")
    speak(questions[10])
    countdown(60)  # 1 phút chuẩn bị
    speak("All right? Remember, you have one to two minutes for this, so don't worry if I stop you. I'll tell you when the time is up. Can you start speaking now")
    countdown(120)  # 2 phút nói
    speak("OK the time is up. let's move to part 3. I will ask you some questions related to the topic. Let's consider")

def part3():
    start_time = time.time()
    for question in questions[11:]:
        if time.time() - start_time > 300:  # 5 phút
            break
        speak(question)
        while True:
            response = listen()
            if not response:
                break
    speak("Thank you. That is the end of the speaking test")


for i in questions:
    print(i)
part1()
part2()
part3()
