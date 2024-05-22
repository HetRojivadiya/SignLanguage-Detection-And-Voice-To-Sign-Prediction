import os
import cv2

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 27
dataset_size = 100

cap = cv2.VideoCapture(0)
for j in range(number_of_classes):
    class_folder = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)
    else:
        # Check the number of images already in the folder
        existing_images = len([name for name in os.listdir(class_folder) if os.path.isfile(os.path.join(class_folder, name))])
        if existing_images >= dataset_size:
            print(f"Class {j} already has {existing_images} images. Skipping...")
            continue  # Move to the next class

    print('Collecting data for class {}'.format(j))

    done = False
    while True:
        ret, frame = cap.read()

        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    print(f'Start capturing images for class {j}')

    counter = existing_images  # Start capturing from the last captured image count
    while counter < dataset_size:
        ret, frame = cap.read()
        # Flip the frame horizontally (mirror view)
        # frame = cv2.flip(frame, 1)  # Flip along the y-axis

        cv2.imshow('frame', frame)
        key = cv2.waitKey(25)
        if key == ord('q'):
            break
        cv2.imwrite(os.path.join(class_folder, '{}.jpg'.format(counter)), frame)

        counter += 1

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
