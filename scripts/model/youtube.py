from yolo_show import yolo_forward
import pafy
import cv2
import os

def youtube_object_recog(youtube_url, names_path, cfg_path, weight_path):
    

    LABELS = open(names_path).read().strip().split("\n")

    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(cfg_path, weight_path)
    
    url = youtube_url
    vPafy = pafy.new(url)
    play = vPafy.getbest(preftype="webm")

    #start the video
    cap = cv2.VideoCapture(play.url)

    counter = 0
    while (True):
        counter += 1
        
        ret,frame = cap.read()
        # (labels, confidences) = yolo_show.yolo_forward(
        #     net, LABELS, 
        #     frame, 0.1, 0.3, 
        #     show_image=True, video_mode=True)
        
        if counter % 3 == 0:
            (labels, confidences) = yolo_forward(
                net, LABELS, 
                frame, 0.1, 0.3, 
                show_image=True, video_mode=True)
        else:
            cv2.imshow('yolo prediction', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break    

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=MTWkfpa-jJw'

    names_path = '/Users/mkz/code/yolo_results/5_clem_emotions_tiny/clem.names'
    cfg_path = '/Users/mkz/code/yolo_results/5_clem_emotions_tiny/clem-yolov3-tiny.cfg'
    weight_path = '/Users/mkz/code/yolo_results/5_clem_emotions_tiny/clem-yolov3-tiny2_best.weights' 
    # names_path = '/Users/mkz/Google Drive/ai-camp/project_aieio/zk/zk2.names'
    # cfg_path = '/Users/mkz/Google Drive/ai-camp/project_aieio/zk/zk2-yolov3-tiny.cfg'
    # weight_path = '/Users/mkz/Google Drive/ai-camp/project_aieio/zk/backup/zk2-yolov3-tiny_last.weights' 
    # press q to exit
    youtube_object_recog(youtube_url, names_path, cfg_path, weight_path)
     