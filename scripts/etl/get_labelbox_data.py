from PIL import Image
import pandas as pd
from io import BytesIO
import time, os, requests, cv2
import numpy as np
from datetime import datetime

def extract_id_url(csv_path):
    data = pd.read_csv(csv_path)
    rtn_df = pd.DataFrame({
        'local_file_name': data['External ID'],
        'lb_id': data['ID'],
        'lb_url': data['Labeled Data'],
        'label': data['Label']
    })

    return rtn_df


def get_lb_image(row, output_path, total_count):
    img_file_name = row['lb_id'] + '-' + row['local_file_name']
    img_path = os.path.join(output_path, img_file_name)
    
    # test to see if the file exist or not, if so, just skip
    if os.path.exists(img_path):
        print('{} already exists'.format(img_file_name))
        return True

    if row['label'] == 'Skip':
        print('not saving {}'.format(img_file_name))
        return False

    start_time = time.time()
    response = requests.get(row['lb_url'])
    if response.status_code == 200:  # !!!
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        if img_array.size == 0:
            'could not get {}'.format(img_file_name)
            return False
        img = cv2.imdecode(img_array, -1)
        # img = Image.open(BytesIO(response.content))

        try:
            cv2.imwrite(img_path, img)
        except:
            print('could not save image')
            return False
        time.sleep(0.1)
        print('{} is saved'.format(img_file_name))
        print('this took {} seconds'.format(time.time() - start_time))
        return True
    else:
        print('could not get image for {}'.format(img_file_name))
        return False

if __name__ == '__main__':
    output_path = '/Users/mkz/Desktop/lb_data_2019_7_23'
    df = extract_id_url('/Users/mkz/Google Drive/ai-camp/project_aieio/export-2019-07-23.csv')
    
    good_df = df[df['label']!='Skip']
    total_count = len(good_df)

    done_count = 0
    failed_count = 0
    for idx, row in good_df.iterrows():
        result = get_lb_image(row, output_path, total_count)

        if result:
            done_count += 1
        else:
            failed_count += 1

        print('idx: {}, done {}, failed {}, total {}'.format(idx, done_count, failed_count, total_count))
        
    