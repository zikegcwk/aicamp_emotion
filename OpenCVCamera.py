import os  # added
import time
import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")
here = os.getcwd()  # added

img_counter = 0
print("To take an image Type h for Happy, s for Sad, p for Poker Face, and SpaceBar for Standard.(ESC to exit)")
while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 104:
        for x in range(0, 10):  # added
            img_name = "HAPPY{}.png".format(img_counter)  # added
            cv2.imwrite(os.path.join(here, 'images', 'happyface', img_name), frame)  # added
            print("{} SAVED!".format(img_name))
            img_counter += 1
            time.sleep(0.5)
    elif k % 256 == 115:
        for x in range(0, 10):  # added
            img_name = "SAD{}.png".format(img_counter)  # added
            cv2.imwrite(os.path.join(here, 'images', 'sadface', img_name), frame)  # added
            print("{} SAVED!".format(img_name))
            img_counter += 1
            time.sleep(0.5)
    elif k % 256 == 112:
        for x in range(0, 10):  # added
            img_name = "POKER{}.png".format(img_counter)  # added
            cv2.imwrite(os.path.join(here, 'images', 'pokerface', img_name), frame)  # added
            print("{} SAVED!".format(img_name))
            img_counter += 1
            time.sleep(0.5)
    elif k % 256 == 32:
        for x in range(0, 10):  # added
            # SPACE pressed
            img_name = "StandardPicture{}.png".format(img_counter)  # added
            cv2.imwrite(os.path.join(here, 'images', 'standard', img_name), frame)  # added
            print("{} SAVED!".format(img_name))
            img_counter += 1
            time.sleep(0.5)
        # break#added
print("TO RUN AGAIN GO PRESS F5 IN CODING PAGE")  # added
cam.release()

cv2.destroyAllWindows()
