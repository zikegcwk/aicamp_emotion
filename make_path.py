import os
import sys

def make_path(folder_path, file_prefix):
    '''split image files into train and validation dataset. 
        store their paths into txt files
    '''

    file_list = os.listdir(folder_path)

    for file1 in file_list:
        print(folder_path, file1)
    # make sure the file_list only contains file end with .jpg or .png

    # how to open a file in a write mode
        train_f = open(file_prefix + '_train.txt', 'w')
        test_f = open(file_prefix + '_test.txt', 'w')

    # iterate through a list
    
        for idx , img in enumerate(file_list):
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
    args = sys.argv
    # example: 
    # argv[1] = '/Users/mutishuman/Documents/images/happyface'
    # argv[2] = 'happy_bing_
    make_path(argv[1], argv[2])
