import os
import cv2

from ai import yolo_forward, get_yolo_net


def main():

    labels = ['happy', 'neutral', 'surprised', 'angry', 'sad']
    img_dir = os.path.join(os.getcwd(), )
    confidence_level = 0.5
    threshold = 0.3
    img_list = []
    total_counter = 0
    counter = 0

    y_actu = []
    y_pred = []

    net_clement = get_yolo_net(
        '/Users/clementou/stuff/aicamp/yolo_training/clem1/backup/yolov3-tiny.cfg',
        '/Users/clementou/stuff/aicamp/yolo_training/clem1/backup/clem-yolov3-tiny_9000.weights',
        confidence_level=0.5, threshold=0.3)

    for img in os.listdir(img_dir):
        if img.endswith('.jpg') or img.endswith('.png') or img.endswith('.gif'):
            image = cv2.imread(os.path.join(img_dir, img))
            img_detect = yolo_forward(net_clement, labels, image, confidence_level, threshold, save_image=False)
            total_counter += 1
            if img_detect == ([], [], [], []):
                y_pred.append(0)
                continue
            else:
                img_list.append(img_detect)
                print(img_detect)
                counter += 1
                for i in img_detect[0]:
                    y_pred.append(i + 1)
        else:
            continue
    print('\n{} images detected out of {} total'.format(counter, total_counter))

    face_counter = 0
    happy_counter = 0
    neutral_counter = 0
    surprised_counter = 0
    angry_counter = 0
    sad_counter = 0

    for i in img_list:
        face_counter += len(i[0])
        for j in i:
            for k in j:
                if k == 0:
                    happy_counter +=1
                if k == 1:
                    neutral_counter +=1
                if k == 2:
                    surprised_counter +=1
                if k == 3:
                    angry_counter +=1
                if k == 4:
                    sad_counter +=1

    print('{} happy faces detected out of {} total faces'.format(happy_counter, face_counter))
    print('{} poker faces detected out of {} total faces'.format(neutral_counter, face_counter))
    print('{} surprised faces detected out of {} total faces'.format(surprised_counter, face_counter))
    print('{} angry faces detected out of {} total faces'.format(angry_counter, face_counter))
    print('{} sad faces detected out of {} total faces'.format(sad_counter, face_counter))



    # for i in range(107):
    #     y_actu.append(1)
    # confusion_matrix(y_actu, y_pred)


if __name__ == '__main__':
    main()