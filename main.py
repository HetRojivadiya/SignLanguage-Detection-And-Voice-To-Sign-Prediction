from itertools import count
import time
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
import tkinter as tk
import string
import pickle
import cv2
import mediapipe as mp
from tkinter import  messagebox

import Levenshtein



def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def custom_buttonbox(msg, image, choices):
    root = tk.Tk()
    root.title("Custom ButtonBox")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    try:
        img = tk.PhotoImage(file=image)
        img_label = tk.Label(frame, image=img)
        img_label.image = img
        img_label.pack(pady=10)
    except tk.TclError as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        root.destroy()
        return

    msg_label = tk.Label(frame, text=msg)
    msg_label.pack(pady=10)

    buttonbox = tk.Frame(frame)
    buttonbox.pack(pady=10)

    for choice in choices:
        button = tk.Button(buttonbox, text=choice, command=lambda c=choice: on_button_click(root, c))
        button.pack(side=tk.LEFT, padx=5)

    
    center_window(root, 800, 550)

    root.mainloop()

def on_button_click(root, choice):
    root.destroy()
    if choice == "Voice To Sign":
        func()
    elif choice == "Sign Detection":
        signDetection()
    elif choice == "Exit":
        quit()
        




def find_closest_match(input_text, gesture_list):
    min_distance = float('inf')
    closest_match = None

    for gesture in gesture_list:
        distance = Levenshtein.distance(input_text, gesture)
        if distance < min_distance:
            min_distance = distance
            closest_match = gesture

    return closest_match if min_distance / max(len(input_text), len(closest_match)) < 0.4 else None



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import AxesWidget

import os

def display_alphabets(a, arr):
    """Display individual alphabets of the unrecognized string sequentially in a thumbnail gallery"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
            }
            .thumbnail {
                width: 200px;
                height: 200px;
                
            }
            .new-line {
                flex-basis: 100%;
                height: 0;
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <div class="gallery">
    """

    for char in a:
        if char != ' ':
            if char in arr:
                image_path = f"letters/{char}.jpg"
            else:
                image_path = "letters/empty.jpg"
            html_content += f'<img class="thumbnail" src="{image_path}" alt="{char}">'
        else:
            html_content += '<div class="new-line"></div>'  
    
    html_content += """
        </div>
    </body>
    </html>
    """

    with open("image_gallery.html", "w") as html_file:
        html_file.write(html_content)

    
    os.system("start image_gallery.html")  
    
    
    
    




def func():
    r = sr.Recognizer()
    isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'be careful',
                'did you book tickets', 'did you finish homework','do you have money', 'do you want something to drink', 'do you want tea or coffee', 'do you watch TV',
               'dont worry', 'flower is beautiful', 'good afternoon', 'good evening', 'good morning',
               'good question', 'happy journey', 'hello what is your name',
               'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
               'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre',
               'i love to shop', 'i had to say something but I forgot','i like pink colour',
               'i live in nagpur', 'lets go for lunch','nice to meet you',
                'open the door', 'please call me later','please use dustbin dont throw garbage', 'please wait for sometime',
               'shall I help you', 'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up',
               'take care', 'there was traffic jam', 'wait I am thinking', 'what are you doing', 'what is the problem',
               'what is todays date', 'what is your father do', 'what is your job', 'what is your mobile number',
               'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
               'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahmedabad',
               'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'bangalore', 'bihar',
               'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile',
               'dasara', 'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'february', 'friday', 'fruits', 'glass',
               'grapes', 'hello', 'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july',
               'karnataka', 'kerala', 'krishna', 'litre', 'mango', 'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim',
               'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station', 'post office', 'pune', 'punjab',
               'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'south africa', 'story',
               'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa',
               'village', 'voice', 'wednesday', 'weight', 'please wait for sometime', 'what is your mobile number',
               'what are you doing', 'are you busy']

    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)

        try:
            a = r.recognize_google(audio)
            a = a.lower()
            print('You Said: ' + a.lower())
            
            closest_match = find_closest_match(a, isl_gif)

            if closest_match:
                print(f"Closest match found: {closest_match}")
                a = closest_match.lower()

            for c in string.punctuation:
                a = a.replace(c, "")

            if a.lower() == 'goodbye' or a.lower() == 'good bye' or a.lower() == 'bye':
                print("Oops! Time to say goodbye")
                return

            elif a.lower() in isl_gif:
                class ImageLabel(tk.Label):
                    """a label that displays images, and plays them if they are gifs"""

                    def load(self, im):
                        if isinstance(im, str):
                            im = Image.open(im)
                        self.loc = 0
                        self.frames = []

                        try:
                            for i in count(1):
                                self.frames.append(ImageTk.PhotoImage(im.copy()))
                                im.seek(i)
                        except EOFError:
                            pass

                        try:
                            self.delay = im.info['duration']
                        except:
                            self.delay = 100

                        if len(self.frames) == 1:
                            self.config(image=self.frames[0])
                        else:
                            self.next_frame()

                    def unload(self):
                        self.config(image=None)
                        self.frames = None

                    def next_frame(self):
                        if self.frames:
                            self.loc += 1
                            self.loc %= len(self.frames)
                            self.config(image=self.frames[self.loc])
                            self.after(self.delay, self.next_frame)

                root = tk.Tk()
                root.eval('tk::PlaceWindow . center')
                lbl = ImageLabel(root)
                lbl.pack()
                lbl.load(r'ISL_Gifs/{0}.gif'.format(a.lower()))
                root.mainloop()

            else:
                
                display_alphabets(a,arr)
                time.sleep(5)
                
                

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print("An error occurred: {0}".format(e))

def signDetection():
    model_dict = pickle.load(open('./model.p', 'rb'))
    model = model_dict['model']

    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=2)

    labels_dict = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
        10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
        19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26:'Right'
    }

    while True:
        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                data_aux = []
                x_ = []
                y_ = []

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10

                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            cv2.LINE_AA)

        cv2.imshow('frame', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
while True:
    image_path = "logo.png"
    message = "SIGN LANGUAGE ASSISTANT FOR HEARING IMPAIRMENTS"
    choices = ["Voice To Sign", "Sign Detection", "Exit"]
    
    custom_buttonbox(message, image_path, choices)


