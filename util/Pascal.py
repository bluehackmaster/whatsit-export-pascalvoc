import os
import zipfile

from util import Comm, Trans


class Pascal:
    def __init__(self, path):
        self.__path = path

    def execute(self):
        PROJECT_NAME = 'FOODS'
        DATASETS = ['sushi', 'tofu_soup', 'fried_chicken', 'pizza']
        IMAGE = ['image1.jpg', 'image2.jpg']

        print('Create directories')
        PROJECT_PATH = Comm.make_project_directory(self.__path, PROJECT_NAME)
        Comm.make_datasets_directory(self.__path, PROJECT_NAME, DATASETS)

        for a in range(3, 101):
            IMAGE.append('image' + str(a) + '.jpg')

        # Creating a 'label_map.pbtxt' file
        Comm.write_file(os.path.join(PROJECT_PATH, 'data/label_map.pbtxt'), Comm.make_label_map(DATASETS))

        for dataset in DATASETS:
            for image in IMAGE:
                Comm.write_file(os.path.join(PROJECT_PATH, 'dataset/' + dataset + '/Annotations/' + image + '.xml'),
                                Comm.make_image_data(dataset, image, DATASETS))

        train, val = Comm.make_train_and_val(IMAGE)

        print(train, val)
        zip = zipfile.ZipFile(os.path.join(self.__path, PROJECT_NAME + '.zip'), 'w')

        for folder, subfolders, files in os.walk(PROJECT_PATH):
            for file in files:
                print(file)
                zip.write(os.path.join(folder, file),
                          os.path.relpath(os.path.join(folder, file), PROJECT_PATH),
                          compress_type=zipfile.ZIP_DEFLATED)
        zip.close()

        file_url = Trans.upload_file_to_bucket('whatsit-dataset-export', zip.filename,
                                               key=PROJECT_NAME + '/' + PROJECT_NAME + '.zip', is_public=False)

        Comm.delete_directory(self.__path)

        print(file_url)
