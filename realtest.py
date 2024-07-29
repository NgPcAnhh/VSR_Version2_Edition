import cv2
import sys
import threading
import pyttsx3
import time
import randomquestionfull
from queue import Queue
import speech_recognition as sr
import random
import numpy as np
import pyaudio
import wave
from datetime import datetime
import tempfile # file ảo, file tạm thời
import os  # Thao tác với hệ thống tệp
import keyboard


exit_event = threading.Event()
is_reading = threading.Event()
video_switch_queue = Queue()
message_queue = Queue()

audio_folder = os.path.join(tempfile.gettempdir(), 'ielts_speaking_audio')
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

class AudioRecorder:
    def __init__(self, filename):
        self.filename = filename
        self.is_recording = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100

        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        print("Recording started...")

        while self.is_recording:
            data = self.stream.read(CHUNK)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        print("Recording stopped.")

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {self.filename}")

class SpeakingTest:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.questions = []
        self.audio_recorder = None
        self.stop_program = False
        self.key_listener_thread = None
        self.test_completed = False

    def open_folder(path):
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":  # macOS
                subprocess.call(["open", path])
            elif sys.platform.startswith("linux"):  # Linux
                subprocess.call(["xdg-open", path])
            else:
                print(f"Unsupported platform: {sys.platform}")
        except Exception as e:
            print(f"Error opening the folder: {e}")

    def start_main_process(self):
        now = datetime.now()
        filename = os.path.join(audio_folder, f"Mock_Test_recording_{now.strftime('%Y%m%d_%H%M%S')}.wav")

        self.audio_recorder = AudioRecorder(filename)
        record_thread = threading.Thread(target=self.audio_recorder.start_recording)
        record_thread.start()


        try:
            self.main_process()
        finally:
            if not self.stop_program:
                self.stop_program = True
                self.audio_recorder.stop_recording()
                record_thread.join()
                if self.key_listener_thread:
                    self.key_listener_thread.join()

    def main_process(self):
        self.questions = randomquestionfull.main()
        message_queue.put(('display_all_questions', self.questions))

        try:
            self.part1()
            if not self.stop_program:
                self.part2()
            if not self.stop_program:
                self.part3()
            if not self.stop_program:
                self.close_interface()  # Thêm dòng này để tắt giao diện
                sys.exit(1)

        except Exception as e:
            print(f"Error during main process: {str(e)}")

    def speak(self, text):
        if self.stop_program:
            return

        print(f"Speaking: {text}")
        is_reading.set()
        video_switch_queue.put(True)
        self.engine.say(text)
        self.engine.runAndWait()
        is_reading.clear()
        video_switch_queue.put(True)
        time.sleep(1)

    def listen(self, timeout=4):
        if self.stop_program:
            return ""

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
                return self.recognizer.recognize_google(audio)
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return ""

    def countdown(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.stop_program:
                return False
            time.sleep(0.1)
        return True

    def part1(self):
        if self.stop_program:
            return
        original_rate = self.engine.getProperty('rate')

        self.engine.setProperty('rate', 150)
        self.speak(
            "This is the simulated speaking test and I'm your examiner. Can you hear my voice, OK please make sure that your microphone is on and keep your surrounding area silent. You should adjust the volume before the test. Are you ready? OK LET START")
        self.speak("Now, in this first part, I'd like to ask you some questions about yourself")
        exclamations = ["So", "Sounds great", "Ok", "Awesome", "Your idea is good", "Good", "Interesting", "Impressive",
                        "That's wonderful to hear!", "Fascinating", "Wow!", "Amazing!", "Incredible!", "Fantastic!",
                        "Wonderful!", "Excellent!", " ", "Fascinating!", "Interesting!", " ", " ", "Brilliant!", " ",
                        " ", "Impressive!", "Great!", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                        " ", " "]

        start_time = time.time()
        for i, question in enumerate(self.questions[:10]):
            if time.time() - start_time > 300:  # 5 minutes
                break
            if i == 0:
                self.speak(question)
            else:
                self.speak(f"{random.choice(exclamations)}! {question}")

            silence_timer = 0
            last_response_time = time.time()

            while True:
                response = self.listen(timeout=1)  # Listen for 1 second at a time
                current_time = time.time()

                if response:
                    print(f"User response: {response}")
                    silence_timer = 0  # Reset silence timer if user speaks
                    last_response_time = current_time
                else:
                    silence_duration = current_time - last_response_time
                    silence_timer += silence_duration

                    if silence_timer >= 3.5:  # If silence lasts for 3.5 seconds or more
                        break
                    elif silence_duration < 1:  # If silence is less than 1 second
                        silence_timer = 0  # Reset silence timer

                last_response_time = current_time

        self.speak("That is the end of part 1, now we will turn to part 2.")

    def part2(self):
        if self.stop_program:
            return
        original_rate = self.engine.getProperty('rate')

        self.speak(
            "In part 2, I'm going to give you a topic and I'd like you to talk about it for one to two minutes. Before you talk, you'll have one minute to think about what you are going to say. You can make some notes if you wish. Here's some paper and a pencil for making notes, and here's your topic.")
        self.engine.setProperty('rate', 200)

        # Thêm '\n' vào câu hỏi
        formatted_question = self.questions[10].replace('. ', '.\n')

        # Activate split screen with the formatted question
        message_queue.put(('activate_split_screen', formatted_question))

        self.speak(self.questions[10])
        self.engine.setProperty('rate', original_rate)
        self.speak("You will have one minute to prepare, I will tell you when the time is up")
        self.countdown(60)  # 1 minute preparation
        self.speak(
            "All right? Remember, you have one to two minutes for this, so don't worry if I stop you. I'll tell you when the time is up. Can you start speaking now?")

        start_time = time.time()
        pause_counter = 0
        while time.time() - start_time < 120:  # 2 minutes for speaking
            response = self.listen(timeout=1)
            if response:
                print(f"User response: {response}")
                pause_counter = 0  # Reset pause counter if user speaks
            else:
                pause_counter += 1
                if pause_counter >= 5:  # If user pauses for 5 seconds
                    break

        # Deactivate split screen
        message_queue.put(('deactivate_split_screen', ''))

        self.speak("OK, the time is up. Let's move to the next part")

    def part3(self):
        if self.stop_program:
            return

        self.speak(
            "Now we move on to part 3. You've been talking about a topic, and I'd like to discuss with you some general questions related to it.")
        exclamations = ["So", "Sounds great", "Ok", "Awesome", "Your idea is good", "Good", "Interesting", "Impressive",
                        "That's wonderful to hear!", "Fascinating", "Wow!", "Amazing!", "Incredible!", "Fantastic!",
                        "Wonderful!", "Excellent!", " ", "Fascinating!", "Interesting!", " ", " ", "Brilliant!",
                        "Impressive!", "Great!", " ", " ", " ", " ", " ", " ", " "]

        start_time = time.time()
        for i, question in enumerate(self.questions[11:]):
            if time.time() - start_time > 300:  # 5 minutes
                break
            if i == 0:
                self.speak(question)
            else:
                self.speak(f"{random.choice(exclamations)}! {question}")

            silence_duration = 0
            last_response_time = time.time()

            while silence_duration < 4:
                response = self.listen(timeout=2)  # Listen for 2 seconds at a time
                current_time = time.time()

                if response:
                    silence_duration = 0
                    last_response_time = current_time
                    print(f"User response: {response}")
                else:
                    silence_duration = current_time - last_response_time

            print("Moving to next question due to 4 seconds of silence")

        self.speak("That is the end of part 3, and also the end of the speaking test. Thank you")
        self.speak("The speaking test is now complete. Thank you for your time.")

        # Set the test_completed flag to True
        self.test_completed = True

        # Wait for 3 seconds before exiting the program
        time.sleep(3)
        
        # Signal to close the program
        exit_event.set()

    def record_audio(output_file, record_seconds=30):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Recording...")

        frames = []

        for i in range(0, int(RATE / CHUNK * record_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Finished recording.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

def create_split_screen(frame, question):
    height, width = frame.shape[:2]
    new_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Video chiếm 3/4 bên phải
    new_frame[:, width // 4:] = frame[:, :3 * width // 4]

    # Phần còn lại là nền trắng với câu hỏi
    new_frame[:, :width // 4] = [255, 255, 255]  # Nền trắng

    # Thêm câu hỏi vào phần nền trắng bên trái
    lines = question.split('\n')
    y = 50
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.7
    font_thickness = 1
    line_spacing = 40

    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            (text_width, text_height), _ = cv2.getTextSize(test_line, font, font_scale, font_thickness)

            if text_width > width // 4 - 20:
                # Draw the current line
                cv2.putText(new_frame, current_line, (10, y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
                y += line_spacing
                current_line = word
            else:
                current_line = test_line

        # Draw the last line of each paragraph
        cv2.putText(new_frame, current_line, (10, y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
        y += line_spacing + 10  # Extra space between paragraphs

    return new_frame

def run_video_player():
    def play_video(video_path, window_name, split_screen=False, question=""):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return False

        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(960 / fps)

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video if end is reached
                continue

            if split_screen:
                frame = create_split_screen(frame, question)

            cv2.imshow(window_name, frame)

            key = cv2.waitKey(delay) & 0xFF
            if key == ord('`') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1 or exit_event.is_set():
                cap.release()
                cv2.destroyAllWindows()
                sys.exit(0)  # Terminate the entire program

            # Check if video switch is needed
            if not video_switch_queue.empty():
                video_switch_queue.get()
                break

        cap.release()
        return True

    def main():
        window_name = 'Simulated Speaking Mock Test (Computer-based)'
        cv2.namedWindow(window_name, cv2.WND_PROP_VISIBLE)
        cv2.resizeWindow(window_name, 1200, 700)

        videos = []
        examiner1 = ['script/doccauhoi.mp4', 'script/minutesp2.mp4']
        examiner2 = ['script/examiner21.mp4', 'script/examiner22.mp4']
        examiner3 = ['script/examiner31.mp4', 'script/examiner32.mp4']

        random_examiner = random.choice(['examiner1', 'examiner2', 'examiner3'])
        if random_examiner == 'examiner1':
            videos.extend(examiner1) 
        elif random_examiner == 'examiner2':
            videos.extend(examiner2) 
        elif random_examiner == 'examiner3':
            videos.extend(examiner3)
        
        current_video_index = 1  # Start with video2
        split_screen_active = False
        current_question = ""

        try:
            while not exit_event.is_set():
                if not message_queue.empty():
                    message = message_queue.get()
                    if message[0] == 'activate_split_screen':
                        split_screen_active = True
                        current_question = message[1]
                    elif message[0] == 'deactivate_split_screen':
                        split_screen_active = False

                play_video(videos[current_video_index], window_name,
                           split_screen=split_screen_active, question=current_question)
                # Switch video
                current_video_index = 1 - current_video_index

                # Check window status
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    print("Window closed. Exiting program.")
                    break

        except KeyboardInterrupt:
            print("Program interrupted")
        finally:
            cv2.destroyAllWindows()
            sys.exit(0)  # Ensure the program exits

    main()

def run_speaking_test():
    speaking_test = SpeakingTest()
    speaking_test.start_main_process()

thread1 = threading.Thread(target=run_video_player)
thread2 = threading.Thread(target=run_speaking_test)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

if __name__ == "__main__":
    main()