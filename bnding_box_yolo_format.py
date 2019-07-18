import os, json, requests
from PIL import Image
from io import BytesIO
import pandas as pd
import numpy as np
from sys import argv

def get_box_centers_all_emotions(sample_row):
    '''
    input: A dictionary of the format {emotion1: [{geometry_box1: [list of 4 corner coordinates],
                                                   geometry_box1: [list of 4 corner coordinates],
                                                   ...}]
                                       emotion2: [...],
                                       ...
                                       emotionN: [...]
                                       }
    output: A dictionary of the format {emotion1: [(center1 coordinates), (center1 coordinates), ...],
                                        emotion2: [...],
                                        ...
                                        emotionN: [...]
                                       }
    '''

    lab = json.loads(sample_row)
    centers = {}
    for key, val in lab.items():
        lab_df = pd.DataFrame(val)
        centers[key] = lab_df.iloc[:, 0].apply(lambda s: get_box_center(s)).tolist()
    return centers

def get_box_center(box_row):
    '''
    input: A list of 4 coordinates, representing the four corners of the bounding box.
        Each coordinate is a dictionary of {'x': xcoord, 'y': ycoord}
    output: A tuple representing the coordinates of the center of the bounding box, and its width and height.
    '''
    x_coords = []
    y_coords = []
    for item in box_row:
        x_coords.append(item['x'])
        y_coords.append(item['y'])
    x_center = (np.max(x_coords) - np.min(x_coords)) / 2 + np.min(x_coords)
    y_center = (np.max(y_coords) - np.min(y_coords)) / 2 + np.min(y_coords)
    box_width = np.max(x_coords) - np.min(x_coords)
    box_height = np.max(y_coords) - np.min(y_coords)
    return (x_center, y_center, box_width, box_height)

def get_width_height(sample_row):
    response = requests.get(sample_row)
    if response.status_code == 200: # !!!
        img = Image.open(BytesIO(response.content))
    return (img.width, img.height)

def get_yolo_formats(emotion_dict, total_width, total_height):
    '''
    Input: a dictionary of {emotion: [(box_x_center, box_y_center, box_width, box_height),
                                      (box_x_center, box_y_center, box_width, box_height), ...]}
    '''
    yolo_formats_to_write = []
    for emotion, boxes in emotion_dict.items():
#         class_id = label_map['class_id'][label_map['emotion']==emotion].values[0]
        if emotion == 'happy':
            class_id = 1
        else:
            class_id = 0
            
        for box in boxes:
            box_x_center, box_y_center, box_width, box_height = box[0], box[1], box[2], box[3]
            yolo_formats_to_write.append(','.join([str(class_id),
                            str(box_x_center/total_width), str(box_y_center/total_height),
                            str(box_width/total_width), str(box_height/total_height)]))
    return yolo_formats_to_write

script, path_to_coords, filename = argv

# Read raw data into memory
raw = pd.read_csv(os.path.join(path_to_coords, filename))
# label_map = pd.read_csv(os.path.join(path_to_labelMap, 'class_ids.txt'))

# Grab the relevant columns
coords = raw[['External ID', 'Label', 'Labeled Data']]

# Remove the rows with no data
coords = coords[coords['Label'] != 'Skip']

# Grab original image dimension. SLOW!!!
coords['width_height'] = coords['Labeled Data'].apply(lambda row: get_width_height(row)) 
# Extract total width and height of image from tuple.
coords['total_width'] = coords['width_height'].apply(lambda s: int(str(s).split(',')[0][1:]))
coords['total_height'] = coords['width_height'].apply(lambda s: int(str(s).split(',')[1].strip()[:-1]))

# Get box centers for each image sample
coords['Centers'] = coords['Label'].apply(lambda s: get_box_centers_all_emotions(s))

# Save the centers data to file
# coords.to_csv(os.path.join(path_to_coords, 'box_centers.csv'), index=False)
# coords = pd.read_csv(os.path.join(path_to_coords, 'box_centers.csv'))

for (i, cents, w, h) in zip(coords['External ID'],
                          coords['Centers'],
                          coords['total_width'], 
                          coords['total_height']):
    if isinstance(cents, str):
        cents = ast.literal_eval(cents)
    yolo_formats_to_write = get_yolo_formats(cents, w, h)
#     print(yolo_formats_to_write)
#     print()
    with open(i.split('.')[0]+'.txt', 'w') as f:
        for box in yolo_formats_to_write:
            f.write("%s\n" % box)