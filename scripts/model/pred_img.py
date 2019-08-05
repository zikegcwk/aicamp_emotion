from ai import yolo_pred

if __name__ == "__main__":
    
    image_path = '/Users/mkz/Desktop/baby.jpg'
    name_path = '/Users/mkz/code/yolo_results/5_clem_emotions/clem.names'
    cfg_path = '/Users/mkz/code/yolo_results/5_clem_emotions/clem-yolov3.cfg'
    weights_path = '/Users/mkz/code/yolo_results/5_clem_emotions/clem-yolov3_best.weights'

    yolo_pred(image_path, name_path, cfg_path, weights_path)