# basic libs
import os
import cv2
import numpy as np
import ntpath
import pandas as pd
import pickle
# for plotting
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
# custom lib
from ai import yolo_forward, get_yolo_net, yolo_save_img, yolo_pred_list
np.set_printoptions(precision=2)

# if the network does not detect anything, the ouput will be this. 
NO_DETECTION_LABEL = 'no detection'

LABELS = ['happy', 'neutral', 'surprised', 'sad', 'angry', NO_DETECTION_LABEL]
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype='uint8')

def label2id(label):
    return LABELS.index(label)

def get_predictions(image_folder_root='data', \
        names_path='.names', cfg_path='.cfg', weight_path='.weights', confidence_level=0.3, \
        output_file='predictions.pickle'):
    '''
    use yolo to make predictions and save results into a pickle file. 
    output will be a list of : 
        result = {
            'image_path': image_path,
            'class_ids': class_ids,
            'labels': labels,
            'boxes': boxes,
            'confidences': confidences,
            'true_label':  'happy'
        }  

    '''
    
    results = []
    for l in LABELS:
        image_folder_path = os.path.join(image_folder_root, l)
        folder_result = yolo_pred_list(
            image_folder_path, 
            names_path, 
            cfg_path, 
            weight_path, 
            confidence_level=confidence_level, 
            threshold=0.1, 
            save_image=False
        )

        updated_results = []
        for r in folder_result:
            r.update({
                'true_label': l
            })
            updated_results.append(r)

        results += updated_results

    with open(os.path.join(image_folder_root, output_file), 'wb') as f:
        pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)

    return results

def clean_scores(pred_path):
    '''
        load results from get_predictions and return a list that consists of: 
        {
            'truth': 'happy',
            'pred': None,
            'score': 0
        }
    '''

    with open(pred_path, 'rb') as handle:
        results = pickle.load(handle)
    
    data = []
    for row in results:
        row_data = {}
        # get truth
        row_data['truth'] = row['true_label']
        
        # get predictions
        confidences = row['confidences']
        labels = row['labels']
        
        if len(confidences) == 0 or len(labels) == 0:
            row_data['pred'] = NO_DETECTION_LABEL
            row_data['score'] = NO_DETECTION_LABEL
            data.append(row_data)
            continue

        # get the index of having the max confidence 
        # and use that for label prediction        
        max_idx = confidences.index(max(confidences))
        row_data['pred'] = labels[max_idx]
        row_data['score'] = max(confidences)

        data.append(row_data)    
    return data

def get_conf_matrix(data):
    '''take a list of dict that has keys: 'truth', 'pred', 'score',
    and return a confusion matrix
    '''
    df = pd.DataFrame.from_dict(data)
    df['pred_idx'] = df['pred'].apply(label2id)
    df['truth_idx'] = df['truth'].apply(label2id)
    return confusion_matrix(df['truth_idx'], df['pred_idx'])

def plot_confusion_matrix(cm, classes, normalize=False, title='confusion matrix',
                          cmap=plt.cm.rainbow, output_file='confusion_matrix.jpg'):
    '''take confusion matrix, plot it, and save it to file
    '''
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] < thresh else "black", size=14)
    # fig.tight_layout()
    plt.savefig(output_file)
    return ax


def save_pred_image(pred_results):

    # drawing images
    for pred_dict in pred_results:
        image_name = ntpath.basename(pred_dict['image_path'])
        image = cv2.imread(pred_dict['image_path'])
        image_folder = os.path.dirname(pred_dict['image_path'])

        output_folder = os.path.join(image_folder, 'predictions')
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        
        yolo_save_img(
            image, 
            pred_dict['class_ids'], 
            pred_dict['boxes'],
            pred_dict['labels'],
            pred_dict['confidences'], 
            COLORS, 
            os.path.join(
                output_folder, 
                image_name
            )
        )


if __name__ == '__main__':

    # set the parameters
    image_folder_root = '/Users/mkz/Google Drive/ai-camp/project_aieio/test_data'
    confidence_level = 0.3
    # # 5 emotion zk data
    # names_path = '/Users/mkz/code/yolo_results/5_emotions/emotion1.names'
    # cfg_path = '/Users/mkz/code/yolo_results/5_emotions/emotion1_yolov3.cfg'
    # weight_path = '/Users/mkz/code/yolo_results/5_emotions/emotion1_yolov3_last.weights'
    # output_file = 'zk-5-emo.pickle'

    # 5 emotion zk data - tiny
    names_path = '/Users/mkz/code/yolo_results/5_emotions_tiny/emotion1.names'
    cfg_path = '/Users/mkz/code/yolo_results/5_emotions_tiny/emotion1_yolov3_tiny.cfg'
    weight_path = '/Users/mkz/code/yolo_results/5_emotions_tiny/emotion1_yolov3_tiny_final.weights'
    output_file = 'zk-tiny-5-emo'
    
    # # 5 emotion clem data
    # names_path = '/Users/mkz/code/yolo_results/5_clem_emotions/clem.names'
    # cfg_path = '/Users/mkz/code/yolo_results/5_clem_emotions/clem-yolov3.cfg'
    # weight_path = '/Users/mkz/code/yolo_results/5_clem_emotions/clem-yolov3_best.weights'
    # output_file = 'clem-5-emo.pickle'
    
    # # 5 emotion clem data - tiny
    # names_path = '/Users/mkz/code/yolo_results/5_clem_emotions_tiny/clem.names'
    # cfg_path = '/Users/mkz/code/yolo_results/5_clem_emotions_tiny/clem-yolov3-tiny.cfg'
    # weight_path = '/Users/mkz/code/yolo_results/5_clem_emotions_tiny/clem-yolov3-tiny2_best.weights'
    # output_file = 'clem-tiny-5-emo.pickle'

    # predictions = get_predictions(
    #     image_folder_root=image_folder_root,
    #     names_path=names_path,
    #     cfg_path=cfg_path,
    #     weight_path=weight_path,
    #     confidence_level=confidence_level,
    #     output_file=output_file
    # )
    data = clean_scores(os.path.join(image_folder_root, output_file + '.pickle'))
    cm = get_conf_matrix(data)
    plot_confusion_matrix(cm, LABELS, normalize=False, 
        title='confusion matrix',
        cmap=plt.cm.rainbow, 
        output_file=os.path.join(image_folder_root, output_file + '_cm.jpg'))
    # save_pred_image(predictions)

