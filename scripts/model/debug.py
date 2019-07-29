import os
import cv2
from ai import yolo_forward, get_yolo_net, yolo_save_img
import numpy as np


def main():
    '''
    test one image using lib from ai.py
    start with just 3 emotions
    '''
    # set the parameters
    LABELS = ['happy', 'poker', 'surprised']
    image_folder = '/Users/mkz/Google Drive/ai-camp/project_aieio/test_data/surprised'
    all_files = os.listdir(image_folder)
    image_files = [f for f in all_files if f.endswith('.jpg') or f.endswith('.png')]
    cfg_path = '/Users/mkz/code/aicamp/zk-yolov3-tiny.cfg'
    weight_path = '/Users/mkz/code/aicamp/zk-yolov3-tiny_best.weights'
    confidence_level = 0.3
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(10000, 3),
                               dtype='uint8')

    # perform prediction
    yolo_net = get_yolo_net(cfg_path, weight_path)
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        print(image_path)
        image = cv2.imread(image_path)
        (class_ids, labels, boxes, confidences) = yolo_forward(yolo_net, LABELS, image, confidence_level, save_image=False)
        # so there are several possibilities. 
        # if we get the matching id, we will then just output the matching id. 
        # if not getting the matching id, we just output the first one. 
        # but what if there is no id at all? What if that is the case? 
        yolo_save_img(image, class_ids, boxes, labels, confidences, colors, 
            os.path.join(
                image_folder, 
                image_file.split('.')[0] + '_pred.' + image_file.split('.')[1]
            )
        )


if __name__ == '__main__':
    main()