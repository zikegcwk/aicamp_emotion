import os
import sys


def make_path(folder_path, file_prefix, output_path):
    """split image files into train and validation dataset.
        store their paths into txt files
    """

    file_list = os.listdir(folder_path)

    # how to open a file in a write mode
    train_f = open(os.path.join(output_path, file_prefix + '_train.txt'), 'w')
    test_f = open(os.path.join(output_path, file_prefix + '_test.txt'), 'w')

    all_label_files = []
    good_image_files = []
    for file1 in file_list:
        if '.txt' in file1:
            all_label_files.append(file1)
            image_file = file1.split('.txt')[0] + '.png'
            if image_file in file_list:
                good_image_files.append(image_file)
            else:
                print('could not find image file: {}'.format(image_file))

    # iterate through a list
    for idx, img in enumerate(good_image_files):
        img_path = os.path.join(folder_path, img)

        if idx % 9 == 0:
            # write data into a file
            test_f.write(img_path + '\n')
        else:
            train_f.write(img_path + '\n')

    train_f.close()
    test_f.close()


if __name__ == '__main__':
    # inputs
    # example:
    # argv[1] = '/Users/mutishuman/Documents/images/happyface'
    # argv[2] = 'happy_bing
    make_path(sys.argv[1], sys.argv[2], sys.argv[3])
