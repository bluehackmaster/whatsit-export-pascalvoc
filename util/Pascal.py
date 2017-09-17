import os
import zipfile

from util import Comm, Trans


class Pascal:
    def __init__(self, path, project_id):
        self.__path = path
        self.__project_id = project_id

    def execute(self):
        IMAGE = ['image1.jpg', 'image2.jpg']
        labels = []

        response_data = \
            Trans.request_service('GET', 'http://api.whatsit.net/projects/' + self.__project_id + '/trainset', [])[
                'data']
        project_name = response_data['name']
        data_sets = response_data['datasets']

        print('Create directories')
        project_path = Comm.make_project_directory(self.__path, project_name)

        for data_set in data_sets[0]:
            print(data_set)
            # for dataset in DATASETS:
            #     for image in IMAGE:
            #         Comm.write_file(os.path.join(PROJECT_PATH, 'dataset/' + dataset + '/Annotations/' + image + '.xml'),
            #                         Comm.make_image_data(dataset, image, DATASETS))


            for data in data_set['data']:
                try:

                    Comm.make_datasets_directory(self.__path, project_name, data['name'])

                    save_location = Trans.download_file(
                        os.path.join(project_path, 'dataset/' + data['name'] + '/temp.zip'),
                        data['frames'])
                    zip = zipfile.ZipFile(save_location)
                    zip.extractall(os.path.join(project_path, 'dataset/' + data['name'] + '/JPEGImages'))
                    zip.close()
                    print('unzip ' + save_location)
                    Comm.delete_file(save_location)

                    for image in data['images']:
                        labels = Comm.insert_label(labels, image['labels'])
                except:
                    print('Excepted')

        # for a in range(3, 101):
        #     IMAGE.append('image' + str(a) + '.jpg')

        # Creating a 'label_map.pbtxt' file
        Comm.write_file(os.path.join(project_path, 'data/label_map.pbtxt'), Comm.make_label_map(labels))

        zip = zipfile.ZipFile(os.path.join(self.__path, project_name + '.zip'), 'w')

        for folder, subfolders, files in os.walk(project_path):
            for file in files:
                zip.write(os.path.join(folder, file),
                          os.path.relpath(os.path.join(folder, file), project_path),
                          compress_type=zipfile.ZIP_DEFLATED)
        zip.close()

        file_url = Trans.upload_file_to_bucket('whatsit-dataset-export', zip.filename,
                                               key=project_name + '/' + project_name + '.zip', is_public=False)

        Comm.delete_directory(self.__path)
        print(file_url)

        #
        #
        # train, val = Comm.make_train_and_val(IMAGE)
        #
