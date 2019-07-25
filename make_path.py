import os
import sys


def make_path(folder_path, file_prefix, output_path):
    """split image files into train and validation dataset.
        store their paths into txt files
    """

    file_list = os.listdir(folder_path)

    # how to open a file in a write mode
    train_f = open(os.path.join(output_path, file_prefix + '_train.txt'), 'w')
    valid_f = open(os.path.join(output_path, file_prefix + '_valid.txt'), 'w')
    # test_f = open(os.path.join(output_path, file_prefix + '_test.txt'), 'w')

    all_label_files = []
    good_image_files = []
    for file1 in file_list:
        if '.txt' in file1:
            all_label_files.append(file1)
            image_file_png = file1.split('.txt')[0] + '.png'
            image_file_jpg = file1.split('.txt')[0] + '.jpg'
            if image_file_png in file_list:
                good_image_files.append(image_file_png)
            elif image_file_jpg in file_list:
                good_image_files.append(image_file_jpg)
            else:
                print('could not find image file for : {}'.format(file1))

    # iterate through a list
    for idx, img in enumerate(good_image_files):
        img_path = os.path.join(folder_path, img)

        if idx % 8 == 0:
            # write data into a file
            valid_f.write(img_path + '\n')
            print('done writing for img {}'.format(img_path))
        else:
            train_f.write(img_path + '\n')
            print('done writing for img {}'.format(img_path))


    train_f.close()
    print('train saved')
    valid_f.close()
    print('valid saved')


if __name__ == '__main__':
    # inputs
    # example:
    # argv[1] = '/Users/mutishuman/Documents/images/happyface'
    # argv[2] = 'happy_bing
    make_path(sys.argv[1], sys.argv[2], sys.argv[3])
