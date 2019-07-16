# face detection and printing errors to index file

import os
import sys
from shutil import copyfile

import cv2


def label_faces():
    """
    This function detects faces in images in a directory and then places the bounding boxes in a txt file in YOLO
    format.
    It also creates an index file with images where it could not detect a face or detected more than one face for later
    manual labelling.
    """
    # sets the emotion
    try:
        emotion = sys.argv[1]
    except IndexError:
        emotion = 'happy'
        print('Emotion set to {}'.format(emotion))

    # sets the image folder
    try:
        img_folder = sys.argv[2]
    except IndexError:
        print('No image folder entered, exiting program')
        sys.exit(1)
    emotion_folder = os.path.join(img_folder, emotion)
    # checks for an index and a log folder and creates it if it does not exist
    index = open(os.path.join(emotion_folder, 'index.txt'), 'w+')
    log = open(os.path.join(emotion_folder, 'log.txt'), 'w+')

    try:  # sets class-id for labeling bounding boxes, default 0
        class_id = sys.argv[3]
    except IndexError:
        class_id = 0

    try:  # the cascade file includes weights for open-cv to detect faces
        cascade_file = os.path.join(img_folder, 'haarcascade_frontalface_default.xml')
    except OSError:
        print('No cascade file detected, please download and place in directory before running')
        sys.exit(1)

    # cycles through each file in the directory
    for img_file in os.listdir(emotion_folder):
        if img_file.endswith(('.png', '.jpg')):
            face_cascade = cv2.CascadeClassifier(cascade_file)  # face detection idk how it works
            try:
                img = cv2.imread(os.path.join(emotion_folder, img_file))
            except OSError:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            label = open(os.path.join(emotion_folder, img_file.split('.')[0] + '.txt'), 'w')

            for (x, y, w, h) in faces:  # TODO add eye checking to make recognition more accurate
                img_h, img_w = img.shape[:2]
                try:
                    center_x = (x + w / 2) / img_w
                    center_y = (y + h / 2) / img_h
                    rel_w = w / img_w
                    rel_h = h / img_h
                except ZeroDivisionError:
                    continue  # writes to the text file in YOlO format
                label.write('{} {} {} {} {}'.format(class_id, center_x, center_y, rel_w, rel_h))

            if len(faces) > 1:
                index.write('{}\n'.format(img_file))
                log.write('More than 1 face detected in {}'.format(img_file))

            if len(faces) == 0:
                index.write('{}\n'.format(img_file))
                log.write('No faces detected in {}'.format(img_file))

            label.close()
    cv2.destroyAllWindows()
    index.close()


def count_failed():
    # sets the emotion
    try:
        emotion = sys.argv[1]
    except IndexError:
        emotion = 'happy'
        print('Emotion set to {}'.format(emotion))

    # sets the image folder
    try:
        img_folder = sys.argv[2]
    except IndexError:
        print('No image folder entered, exiting program')
        sys.exit(1)
    emotion_folder = os.path.join(img_folder, emotion)
    # checks for an index and a log folder and creates it if it does not exist
    index = open(os.path.join(emotion_folder, 'index.txt'), 'w+')
    log = open(os.path.join(emotion_folder, 'log.txt'), 'w+')

    num_files = 0
    for img_file in os.listdir(emotion_folder):
        if img_file.endswith(('.png', '.jpg')):
            num_files += 1

    with index:
        failed = sum(1 for _ in index)
        print('{} failed detections'.format(failed))  # return failed detections
        log.write('{} failed detections\n'.format(failed))
        print('{} successful detections'.format(num_files - failed))  # return successful detections
        log.write('{} successful detections'.format(num_files - failed))
        percent_failed = '%.2f' % float(failed / num_files)
        print('{}% failed'.format(percent_failed))  # return percentage failed detections
        log.write('{}% failed'.format(percent_failed))


def move_failed():
    # sets the emotion
    try:
        emotion = sys.argv[1]
    except IndexError:
        emotion = 'happy'
        print('Emotion set to {}'.format(emotion))

    # sets the image folder
    try:
        img_folder = sys.argv[2]
    except IndexError:
        print('No image folder entered, exiting program')
        sys.exit(1)
    emotion_folder = os.path.join(img_folder, emotion)

    # checks for an index and a log folder and creates it if it does not exist
    log = open(os.path.join(emotion_folder, 'log.txt'), 'w+')

    try:  # create folder to store copies of failed images
        os.mkdir(os.path.join(img_folder, 'failed' + emotion))
        print('Successfully created failed image folder')
    except OSError:
        print('Failed to create failed image folder')
        sys.exit(1)
    else:
        failed_folder = os.path.join(img_folder, 'failed' + emotion)
        print('Existing failed image folder found')
    index = open(os.path.join(emotion_folder, 'index.txt'), 'r')

    lines = [line.rstrip('\n') for line in index]
    for file in lines:
        old_loc = os.path.join(emotion_folder, file)
        new_loc = os.path.join(failed_folder, file)
        copyfile(old_loc, new_loc)
        log.write('Moved {} to {}'.format(old_loc, new_loc))


if __name__ == '__main__':
    label_faces()
    count_failed()
    move_failed()
