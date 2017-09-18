import os
import zipfile

from util import Comm, Trans


class Pascal:
    def __init__(self, path, project_id):
        self.__path = path
        self.__project_id = project_id

    def execute(self):
        labels = []

        response_data = \
            Trans.request_service('GET', 'http://api.whatsit.net/projects/' + self.__project_id + '/trainset', [])[
                'data']
        project_name = response_data['name']
        data_sets = response_data['datasets']

        project_path = Comm.make_project_directory(self.__path, project_name)
        print('Created directories: ' + project_path)

        for data_set in data_sets[0]:
            for data in data_set['data']:
                try:
                    data_set_name = data['name']
                    data_set_path = os.path.join(project_path, 'dataset/' + data['name'])
                    print('creating data set folder')
                    Comm.make_datasets_directory(self.__path, project_name, data_set_name)

                    # TODO 압축 / 압축 해제 모듈화 작업
                    # save_location = Trans.download_file(
                    #     os.path.join(data_set_path, '/temp.zip'),
                    #     data['frames'])
                    save_location = '/Users/bluehack/Downloads/gonghyojin_final.zip'
                    zips = zipfile.ZipFile(save_location)

                    extract_path = os.path.join(data_set_path, 'temp')
                    zips.extractall(extract_path)
                    zips.close()

                    for image in data['images']:
                        if len(image['objects']) > 0:
                            image_file_name = image['name']
                            Comm.move_file(os.path.join(extract_path, image_file_name),
                                           os.path.join(os.path.join(data_set_path, 'JPEGImages'), image_file_name))
                            labels = Comm.insert_label(labels, image['labels'])
                            Comm.write_file(
                                os.path.join(project_path,
                                             'dataset/' + data_set_name + '/Annotations/' + image_file_name + '.xml'),
                                Comm.make_image_data(data_set_name, image))

                    Comm.delete_directory([extract_path])

                except Exception as ex:
                    print('Excepted' + ex)

        # Creating a 'label_map.pbtxt' fileR
        Comm.write_file(os.path.join(project_path, 'data/label_map.pbtxt'), Comm.make_label_map(labels))

        print('Compressing export files.')
        zip = zipfile.ZipFile(os.path.join(self.__path, project_name + '.zip'), 'w')

        for folder, subfolders, files in os.walk(project_path):
            for file in files:
                zip.write(os.path.join(folder, file),
                          os.path.relpath(os.path.join(folder, file), project_path),
                          compress_type=zipfile.ZIP_DEFLATED)
        zip.close()

        print('Uploading the export zip file to bucket.')
        file_url = Trans.upload_file_to_bucket('whatsit-dataset-export', zip.filename,
                                               key=project_name + '/' + project_name + '.zip', is_public=False)

        print('Deleting temporary files for exporting.')
        Comm.delete_directory([self.__path])
        print(file_url)

        #
        #
        # train, val = Comm.make_train_and_val(IMAGE)
        #
