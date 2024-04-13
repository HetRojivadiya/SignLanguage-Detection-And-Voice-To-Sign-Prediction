import speech_recognition as sr
import Levenshtein
import cv2
import os

def recognize_voice():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 2 seconds")
        recorded_audio = recognizer.listen(source, timeout=3)
        print("Done recording")

    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        print("Decoded Text : {}".format(text))
        return text.lower()

    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

def compare_strings(input_text, predefined_strings_and_images):
    similarities = [(Levenshtein.distance(input_text, predefined), predefined, image_path) for predefined, image_path in predefined_strings_and_images]
    similarities.sort()  
    return similarities[0][1], similarities[0][2] 

def main():
    predefined_strings_and_images = [
        ("hello", "./images/hello.jpg"),
        
        ("goodbye", "./images/bye.jpg"),
        ("kem cho",'./images/what.jpg'),
        ("what",'./images/what.jpg'),
        ("kya javu che",'./images/where.jpg'),
        ("where are you going",'./images/where.jpg'),
        ("nanu",'./images/small.jpg'),
        ("little",'./images/small.jpg'),
        ("small",'./images/small.jpg'),
        ("tiny",'./images/small.jpg'),
        ("say",'./images/say.jpg'),
        ("talk",'./images/say.jpg'),
        ("perfect",'./images/perfect.jpg'),
        ("saras",'./images/perfect.jpg'),
        ("khub saras",'./images/perfect.jpg'),
        ("and","./images/and.jpg"),
        ("ane","./images/and.jpg"),
        ("all good","./images/kemcho.jpg"),
        ("badhu barobar","./images/kemcho.jpg"),
        
    ]

    while True:
        input_text = recognize_voice()
        if input_text and input_text.lower() == 'q':
            print("Exiting the program.")
            break

        if input_text:
            most_similar_string, corresponding_image_path = compare_strings(input_text, predefined_strings_and_images)
            print("Most matching string: {}".format(most_similar_string))

            if corresponding_image_path and os.path.exists(corresponding_image_path):
                print("Opening corresponding image: {}".format(corresponding_image_path))
                image = cv2.imread(corresponding_image_path)
                cv2.namedWindow("Corresponding Image", cv2.WINDOW_NORMAL)
                cv2.setWindowProperty("Corresponding Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow("Corresponding Image", image)
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                # Break the loop if the 'q' key is pressed
                if key == ord('q'):
                    print("Exiting the program.")
                    break
            else:
                print("No corresponding image found.")

if __name__ == "__main__":
    main()