import os  # added import time import numpy as np
import sys
import time

import cv2


def main():
    """This program is to take multiple images for AIEIO when an assigned key is pressed
    --- You may adjust the amount of pictures you want for each press by changing the
    assigned range :)
    """

    emotion = sys.argv[1]
    here = os.getcwd()  # added

    path = os.path.join(here, 'images', emotion)
    if os.path.isdir(path):
        print("Directory was not created since %s already exists" % path)
    else:
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

    try:  # sets image counter to avoid overwriting old images
        img_counter = int(max(os.listdir(path)).split(".png")[0].split("_")[1]) + 1
        print("Starting image counter at %s" % img_counter)
    except ValueError:
        img_counter = 0
        print("No files detected, starting counter at 0")

    cam = cv2.VideoCapture(0)
    print("Press space to take an image, esc or ctrl + c to exit. Currently taking %s pictures." % emotion)

    cv2.namedWindow("OpenCVCamera")

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k % 256 == 27:  # esc pressed
            print("Escape hit, closing...")
            break
        if k % 256 == 32:  # space pressed
            for x in range(0, 50):
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                cv2.waitKey(1)
                img_name = "{}_{}.png".format(emotion, str(img_counter).zfill(4))
                cv2.imwrite(os.path.join(here, 'images', emotion, img_name), frame)
                print("{} Saved".format(img_name))
                img_counter += 1
                time.sleep(.2)
    cam.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
