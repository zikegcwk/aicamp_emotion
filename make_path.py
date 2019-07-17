import os

def make_path(folder_path, happy_face):

    file_list = os.listdir(folder_path)

    for file1 in file_list:
        print(folder_path, file1)
    # make sure the file_list only contains file end with .jpg or .png

    # how to open a file in a write mode
        train_f = open(happy_face + '_train.txt', 'w')
        test_f = open(happy_face + '_test.txt', 'w')

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
    folder_path = '/Users/mutishuman/Documents/images/happyface'
    happy_face = 'happy_face'
    file_list = os.listdir(folder_path)
    for file1 in file_list:
        print(folder_path, file1)

    make_path(folder_path, happy_face)
