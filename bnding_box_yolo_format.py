import ast
import json
import os
from io import BytesIO
from sys import argv

import cv2
import numpy as np
import pandas as pd
import requests
from PIL import Image


def get_box_centers_all_emotions(sample_row):
    """
    input: A dictionary of the format
    {
        emotion1: [{geometry_box1: [list of 4 corner coordinates],
                    geometry_box1: [list of 4 corner coordinates],
                    ...}]
        emotion2: [...],
        ...
        emotionN: [...]
    }
    output: A dictionary of the format
        {
            emotion1: [(center1 coordinates), (center1 coordinates), ...],
            emotion2: [...],
            ...
            emotionN: [...]
        }
    """

    lab = json.loads(sample_row)
    centers = {}
    for key, val in lab.items():
        lab_df = pd.DataFrame(val)
        centers[key] = lab_df.iloc[:, 0].apply(lambda s: get_box_center(s)).tolist()
    return centers


def get_box_center(box_row):
    """
    input: A list of 4 coordinates, representing the four corners of the bounding box.
        Each coordinate is a dictionary of {'x': xcoord, 'y': ycoord}
    output: A tuple representing the coordinates of the center of the bounding box, and its width and height.
    """
    x_coords = []
    y_coords = []
    for item in box_row:
        x_coords.append(item['x'])
        y_coords.append(item['y'])
    x_center = (np.max(x_coords) - np.min(x_coords)) / 2 + np.min(x_coords)
    y_center = (np.max(y_coords) - np.min(y_coords)) / 2 + np.min(y_coords)
    box_width = np.max(x_coords) - np.min(x_coords)
    box_height = np.max(y_coords) - np.min(y_coords)
    return x_center, y_center, box_width, box_height


def get_width_height_labelbox(sample_row):
    response = requests.get(sample_row)
    if response.status_code == 200:  # !!!
        img = Image.open(BytesIO(response.content))
        return img.width, img.height
    else:
        return 0, 0


def get_width_height_local(file_name, image_folder_path, labelbox_url):
    file_path = os.path.join(image_folder_path, file_name)

    img_width, img_height = 0, 0
    img = cv2.imread(file_path)
    if img is not None:
        img_height, img_width, channels = img.shape
        print('returned local dimensions for {}: ({}, {})'.format(file_name, img_width, img_height))
    else:
        print('could not load image for {}'.format(file_name))

    return img_width, img_height


def get_yolo_formats(emotion_dict, total_width, total_height):
    """
    Input: a dictionary of
        {emotion: [
            (box_x_center, box_y_center, box_width, box_height),
            (box_x_center, box_y_center, box_width, box_height), ...]
        }
    """
    yolo_formats_to_write = []

    if total_width == 0 or total_height == 0:
        print('have 0 height or width. skipping file')
        return yolo_formats_to_write

    for emotion, boxes in emotion_dict.items():
        for box in boxes:
            # only do happy and neutral for now. Will do more emotions later.
            if emotion == 'happy':
                class_id = 0
                box_x_center, box_y_center, box_width, box_height = box[0], box[1], box[2], box[3]
                yolo_formats_to_write.append(' '.join([str(class_id),
                                                       str(box_x_center / total_width),
                                                       str(box_y_center / total_height),
                                                       str(box_width / total_width), str(box_height / total_height)]))
            if emotion == 'neutral':
                class_id = 1
                box_x_center, box_y_center, box_width, box_height = box[0], box[1], box[2], box[3]
                yolo_formats_to_write.append(' '.join([str(class_id),
                                                       str(box_x_center / total_width),
                                                       str(box_y_center / total_height),
                                                       str(box_width / total_width), str(box_height / total_height)]))
            if emotion == 'surprised':
                class_id = 2
                box_x_center, box_y_center, box_width, box_height = box[0], box[1], box[2], box[3]
                yolo_formats_to_write.append(' '.join([str(class_id),
                                                       str(box_x_center / total_width),
                                                       str(box_y_center / total_height),
                                                       str(box_width / total_width), str(box_height / total_height)]))
            if emotion == 'angry':
                class_id = 3
                box_x_center, box_y_center, box_width, box_height = box[0], box[1], box[2], box[3]
                yolo_formats_to_write.append(' '.join([str(class_id),
                                                       str(box_x_center / total_width),
                                                       str(box_y_center / total_height),
                                                       str(box_width / total_width), str(box_height / total_height)]))
            if emotion == 'sad':
                class_id = 4
                box_x_center, box_y_center, box_width, box_height = box[0], box[1], box[2], box[3]
                yolo_formats_to_write.append(' '.join([str(class_id),
                                                       str(box_x_center / total_width),
                                                       str(box_y_center / total_height),
                                                       str(box_width / total_width), str(box_height / total_height)]))

    return yolo_formats_to_write


if __name__ == '__main__':

    script_name, path_to_coords, image_folder_path = argv

    # Read raw data into memory
    raw = pd.read_csv(path_to_coords)

    # Grab the relevant columns
    # External ID is the file name of the image
    # Label is the labeled data
    # Labeled Data is the URL of the image stored in label box.
    coords = raw[['External ID', 'Label', 'Labeled Data']]

    # Remove the rows with no data
    coords = coords[coords['Label'] != 'Skip']

    # Grab original image dimension. 
    # first try local file, if no local file, requests labelbox. 
    # if no image, return 0, which we will skip the file.
    coords['width_height'] = coords.apply(
        lambda row: get_width_height_local(row['External ID'], image_folder_path, row['Labeled Data']),
        axis=1
    )

    # Extract total width and height of image from tuple.
    coords['total_width'] = coords['width_height'].apply(lambda s: int(str(s).split(',')[0][1:]))
    coords['total_height'] = coords['width_height'].apply(lambda s: int(str(s).split(',')[1].strip()[:-1]))

    # Get box centers for each image sample
    coords['Centers'] = coords['Label'].apply(lambda s: get_box_centers_all_emotions(s))

    # Save the centers data to file
    # coords.to_csv(os.path.join(path_to_coords, 'box_centers.csv'), index=False)
    # coords = pd.read_csv(os.path.join(path_to_coords, 'box_centers.csv'))

    processed_count = 0
    failed_count = 0
    for (img_file_name, cents, w, h) in zip(coords['External ID'],
                                            coords['Centers'],
                                            coords['total_width'],
                                            coords['total_height']):

        if isinstance(cents, str):
            cents = ast.literal_eval(cents)

        yolo_formats_to_write = get_yolo_formats(cents, w, h)
        print(yolo_formats_to_write)

        if not yolo_formats_to_write:
            failed_count += 1
            print('---xxx failed for file {}'.format(img_file_name))
        else:
            # save results
            file_name = img_file_name.split('.')[0] + '.txt'
            with open(os.path.join(image_folder_path, file_name), 'w') as f:
                for box in yolo_formats_to_write:
                    f.write('%s\n' % box)

                print('--->>>> saved for file {}'.format(img_file_name))
        processed_count += 1
        print('processed: {}, failed: {}'.format(processed_count, failed_count))
