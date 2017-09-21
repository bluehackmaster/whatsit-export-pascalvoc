from collections import defaultdict
from os import path

from util.Comm import *
from util.Trans import *


class Pascal:
    def __init__(self, path, project_id):
        self.__path = path
        self.__project_id = project_id

    def execute(self):
        labels = []

        response_data = \
            request_service('GET', 'http://api.whatsit.net/projects/' + self.__project_id + '/trainset', [])['data']

        project_name = response_data['name']
        data_sets = response_data['datasets']

        project_path = make_project_directory(self.__path, project_name)
        print('Created directories: ' + project_path)

        for data_set in data_sets:
            for data in data_set['data']:
                label_sets = defaultdict(list)
                data_set_name = data['name']
                data_set_path = path.join(project_path, 'dataset/' + data['name'])
                print('creating data set folder')
                make_datasets_directory(self.__path, project_name, data_set_name)
                save_location = download_file(
                    path.join(data_set_path, 'temp.zip'),
                    data['frames'])
                extract_path = path.join(data_set_path, 'temp')

                uncompress_files(save_location, extract_path)

                for image in data['images']:
                    if len(image['objects']) > 0:
                        image_file_name = image['name']
                        move_file(path.join(extract_path, image_file_name),
                                  path.join(path.join(data_set_path, 'JPEGImages'), image_file_name))
                        labels = insert_label(labels, image['labels'])
                        object_data, label_sets = make_image_data(data_set_name, image, label_sets)
                        write_file(
                            path.join(project_path,
                                      'dataset/' + data_set_name + '/Annotations/' + image_file_name + '.xml'),
                            object_data)
                delete_directory([extract_path])
                delete_file(save_location)
                for label in label_sets:
                    train, val = make_train_and_val(label_sets[label])
                    write_file(path.join(data_set_path, 'ImageSets/Main/' + label + '_train.txt'),
                               make_image_sets(train))
                    write_file(path.join(data_set_path, 'ImageSets/Main/' + label + '_val.txt'), make_image_sets(val))

        # Creating a 'label_map.pbtxt' fileR
        write_file(path.join(project_path, 'data/label_map.pbtxt'), make_label_map(labels))

        print('Compressing export files.')
        compressed_file_path = compress_files(project_path, path.join(self.__path, project_name + '.zip'))
        print('Uploading the export zip file to bucket.' + compressed_file_path)
        file_url = upload_file_to_bucket('whatsit-dataset-export', compressed_file_path,
                                         key=self.__project_id + '/' + project_name + '.zip', is_public=True)
        print('Deleting temporary files for exporting.')
        delete_directory([self.__path])
        print(file_url)

        params = {
            "exports": {
                "uri": file_url,
                "format": "pascalvoc"
            }
        }
        print(request_service('PUT', 'http://api.whatsit.net/projects/' + self.__project_id, params))
