# USAGE
# python yolo.py --image images/baggage_claim.jpg --yolo yolo-coco

# import the necessary packages
import numpy as np
import time
import cv2
import os

def yolo_forward(net, LABELS, image, confidence_level, threshold, show_image=True, video_mode=False):
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(10000, 3),
        dtype="uint8")

    # load our input image and grab its spatial dimensions
    # image = cv2.imread(image_path)
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
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
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_level, threshold)

    if len(idxs) > 0:
        good_class_ids = idxs.flatten()
        good_labels = [LABELS[i] for i in good_class_ids]
        good_boxes = [boxes[i] for i in good_class_ids]
        good_confidences = [confidences[i] for i in good_class_ids]
    else:
        good_class_ids = []
        good_labels = []
        good_boxes = []
        good_confidences = []

    if show_image:
        if video_mode:
            show_img(image, good_class_ids, good_boxes, good_labels, good_confidences, COLORS, video_mode=True)
        else:
            show_img(image, good_class_ids, good_boxes, good_labels, good_confidences, COLORS)


    return (good_labels, good_confidences)
            
def show_img(image, class_ids, boxes, labels, confidences, COLORS, video_mode=False):
    
    if len(class_ids) > 0:
        for i, box in enumerate(boxes):
            # extract the bounding box coordinates
            (x, y) = (box[0], box[1])
            (w, h) = (box[2], box[3])
                
            # draw a bounding box rectangle and label on the image
            
            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(labels[i], confidences[i])
            print(text)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    if video_mode:
        cv2.imshow("yolo prediction", image)
        print('video mode')
        cv2.waitKey(1)
    else:
        cv2.imshow("yolo prediction", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1)


def yolo_pred(image_path, names_file, cfg_file, weight_file, confidence_level=0.5, threshold=0.3, show_image=True):
    if not names_file or not cfg_file or not weight_file:
        raise Exception('missing inputs. See file.')

    yolo_path = os.getcwd()
    # load the COCO class labels our YOLO model was trained on
    labelsPath = os.path.sep.join([yolo_path, "data", names_file])
    LABELS = open(labelsPath).read().strip().split("\n")

    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weight_file])
    configPath = os.path.sep.join([yolo_path, 'cfg', cfg_file])

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    image = cv2.imread(image_path)
    (labels, confidences) = yolo_forward(
        net, LABELS, 
        image, confidence_level, threshold, 
        show_image=show_image)

    return (labels, confidences)


def img_pred(image, names_file, cfg_file, weight_file, confidence_level=0.5, threshold=0.3, show_image=True):
    if not names_file or not cfg_file or not weight_file:
        raise Exception('missing inputs. See file.')

    yolo_path = os.getcwd()
    # load the COCO class labels our YOLO model was trained on
    labelsPath = os.path.sep.join([yolo_path, "data", names_file])
    LABELS = open(labelsPath).read().strip().split("\n")

    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weight_file])
    configPath = os.path.sep.join([yolo_path, 'cfg', cfg_file])

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    
    (labels, confidences) = yolo_forward(
        net, LABELS, 
        image, confidence_level, threshold, 
        show_image=show_image)

    return (labels, confidences)


def yolo_video(names_path, cfg_path, weight_path, confidence_level=0.5, threshold=0.3):
    
    LABELS = open(names_path).read().strip().split("\n")
    net = cv2.dnn.readNetFromDarknet(cfg_path, weight_path)
    print("[INFO] done loading YOLO ...")
    
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("yolo prediction")
    while True:
        ret, image = cam.read()
        # time.sleep(1)
        (labels, confidences) = yolo_forward(
            net, LABELS, 
            image, confidence_level, threshold, 
            show_image=True, video_mode=True)
    
        
        

def yolo_pred_list(image_folder_path, names_file, cfg_file, weight_file, confidence_level=0.5, threshold=0.3, show_image=True):

    all_paths = os.listdir(image_folder_path)
    image_paths = [os.path.join(image_folder_path, f) for f in all_paths if '.jpg' in f]

    image_paths.sort()

    yolo_path = os.getcwd()
    # load the COCO class labels our YOLO model was trained on
    labelsPath = os.path.sep.join([yolo_path, "data", names_file])
    LABELS = open(labelsPath).read().strip().split("\n")

    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weight_file])
    configPath = os.path.sep.join([yolo_path, 'cfg', cfg_file])

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    for image_path in image_paths:
        print('++++++++++New Prediction+++++++++')
        print(image_path)
        image = cv2.imread(image_path)
        (labels, confidences) = yolo_forward(net, LABELS, image, confidence_level, threshold, show_image=show_image)
        
        print('labels: {}, confidences: {}'.format(labels, confidences))




