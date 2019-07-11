import cv2
import os #added import time import numpy as np
import time
def main():
    '''This program is to take multiple images for AIEIO when an asigned key is pressed
    --- You may adjust the amount of pictures you want for each press by changing the
    assinged range :)
    '''
    cam = cv2.VideoCapture(0)
    print("To take an image Type h for Happy, s for Sad, p for Poker Face, and SpaceBar for Standard.(ESC to exit or CTRl C )")

    cv2.namedWindow("test")
    here = os.getcwd()#added
    img_counter = 0
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        if k%256==104:
            Session_Name_for_img = input('Please input your name followed by your Session number = ')
            for x in range(0, 150):
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                cv2.waitKey(1)
                img_name = "opencv_frame_HAPPY_{}_{}.png".format(img_counter,Session_Name_for_img)#added
                cv2.imwrite(os.path.join(here, 'images', 'happyface', img_name), frame)#added
                print("{} SAVED!".format(img_name))
                img_counter += 1
                time.sleep(.2)
        
        if k%256==115:
            Session_Name_for_img = input('Please input your name followed by your Session number = ')
            for x in range(0, 150):
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                cv2.waitKey(1)
                img_name = "opencv_frame_SAD_{}_{}.png".format(img_counter,Session_Name_for_img)#added
                cv2.imwrite(os.path.join(here, 'images', 'sadface', img_name), frame)#added
                print("{} SAVED!".format(img_name))
                img_counter += 1
                time.sleep(.3)
           
        if k%256==112:
            Session_Name_for_img = input('Please input your name followed by your Session number = ')
            for x in range(0, 150):
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                cv2.waitKey(1)
                img_name = "opencv_frame_POKER_{}_{}.png".format(img_counter,Session_Name_for_img)#added
                cv2.imwrite(os.path.join(here, 'images', 'pokerface', img_name), frame)#added
                print("{} SAVED!".format(img_name))
                img_counter += 1
                time.sleep(.3)
            
        if k%256 == 109:
            Session_Name_for_img = input('Please input your name followed by your Session number = ')
            for x in range(0, 150):
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                cv2.waitKey(1)
                img_name = "opencv_frame_MADFACE_{}_{}.png".format(img_counter,Session_Name_for_img)#added
                cv2.imwrite(os.path.join(here, 'images', 'madface', img_name), frame)#added
                print("{} SAVED!".format(img_name))
                img_counter += 1
                time.sleep(.3)
             
             
        if k%256 == 32:
            Session_Name_for_img = input('Please input your name followed by your Session number = ')
            for x in range(0, 150):
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                cv2.waitKey(1)
                img_name = "opencv_frame_StandardPicture_{}_{}.png".format(img_counter,Session_Name_for_img)#added
                cv2.imwrite(os.path.join(here, 'images', 'standard', img_name), frame)#added
                print("{} SAVED!".format(img_name))
                img_counter += 1
                time.sleep(.3)
           # break#added
            
    print("TO RUN AGAIN GO PRESS F5 IN CODING PAGE ")#added
    cam.release()

    cv2.destroyAllWindows()
if __name__== "__main__":
    main()