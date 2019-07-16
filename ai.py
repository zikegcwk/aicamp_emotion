# import the necessary packages
import time

import cv2
import numpy as np


def yolo_forward(net, labels, image, confidence_level, threshold, save_image=False):
    """
    forward data through YOLO network
    """

    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(10000, 3),
                               dtype="uint8")

    # grab image spatial dimensions
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    # also time it
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layer_outputs = net.forward(ln)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    class_ids = []

    # loop over each of the layer outputs
    for output in layer_outputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confidence_level:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    # idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_level, threshold)

    labels = [labels[i] for i in class_ids]

    if save_image:
        save_img(image, class_ids, boxes, labels, confidences, colors, 'predictions.jpg')

    return class_ids, labels, boxes, confidences


def yolo_save_img(image, class_ids, boxes, labels, confidences, colors, file_path):
    """
    save a image with bounding boxes
    """
    for i, box in enumerate(boxes):
        # extract the bounding box coordinates
        (x, y) = (box[0], box[1])
        (w, h) = (box[2], box[3])

        # draw a bounding box rectangle and label on the image
        color = [int(c) for c in colors[class_ids[i]]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(labels[i], confidences[i])
        print(text)
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imwrite(file_path, image)
    return image


def get_yolo_net(cfg_path, weight_path, confidence_level=0.5, threshold=0.3):
    """
    return YOLO net.
    run this function when app starts to load the net.
    """

    if not cfg_path or not weight_path:
        raise Exception('missing inputs. See file.')

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(cfg_path, weight_path)

    return net
