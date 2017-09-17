import math
import os
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement


# TODO : Convert to class from this for saving project name(to reuse).

# noinspection PyPep8Naming
def check_and_create_directory(paths):
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)


def delete_directory(path):
    shutil.rmtree(path)


def delete_file(path):
    os.remove(path)


def insert_label(origin, labels):
    for label in labels:
        try:
            if origin.index(label) == 0:
                print(label + ' is in list')
        except ValueError:
            origin.append(label)

    return origin


def make_project_directory(path, project):
    PROJECT_TEMP_PATH = os.path.join(path, project)
    folders = ['data', 'models', 'models/model', 'models/model/eval', 'models/model/train', 'dataset']

    check_and_create_directory([path, PROJECT_TEMP_PATH])

    for folder in folders:
        os.mkdir(os.path.join(PROJECT_TEMP_PATH, folder))

    return PROJECT_TEMP_PATH


def make_datasets_directory(path, project, dataset):
    PROJECT_TEMP_PATH = os.path.join(path, project)
    print(dataset)
    if dataset is not None:
        folders = ['dataset/' + dataset, 'dataset/' + dataset + '/Annotations',
                   'dataset/' + dataset + '/JPEGImages', 'dataset/' + dataset + '/ImageSets',
                   'dataset/' + dataset + '/ImageSets/Main']

        for folder in folders:
            os.mkdir(os.path.join(PROJECT_TEMP_PATH, folder))


def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


def make_label_map(labels):
    rslt = ''

    for idx, val in enumerate(labels):
        rslt += 'item { \n id: ' + str(idx + 1) + '\n name: \'' + val + '\'\n}\n\n'

    return rslt.encode('utf-8')


def make_image_data(dataset, image, objects):
    annotation = Element('annotation')
    SubElement(annotation, 'folder').text = dataset
    SubElement(annotation, 'filename').text = image
    SubElement(annotation, 'segmented').text = '0'

    source = Element('source')
    SubElement(source, 'database').text = 'The VOC2008 Database'
    SubElement(source, 'annotaion').text = 'PASCAL VOC2008'
    SubElement(source, 'image').text = '아'

    size = Element('size')
    SubElement(size, 'width').text = '371'
    SubElement(size, 'height').text = '500'
    SubElement(size, 'depth').text = '3'

    annotation.append(source)
    annotation.append(size)

    for idx, object in enumerate(objects):
        annotation.append(make_image_object(idx))

    return ET.tostring(annotation, encoding='UTF-8', method='xml')


def make_image_object(abc):
    object = Element('object')

    SubElement(object, 'name').text = 'bicycle' + str(abc)
    SubElement(object, 'pose').text = 'Frontal'
    SubElement(object, 'truncated').text = '1'
    SubElement(object, 'occluded').text = '0'
    SubElement(object, 'difficult').text = '0'

    bndbox = Element('bndbox')
    SubElement(bndbox, 'xmin').text = '64'
    SubElement(bndbox, 'ymin').text = '390'
    SubElement(bndbox, 'xmax').text = '354'
    SubElement(bndbox, 'ymax').text = '500'

    object.append(bndbox)

    return object


def make_train_and_val(files):
    total_count = len(files)
    train_count = math.trunc(total_count * 0.8)
    trains = []
    vals = []
    for idx, val in enumerate(files):
        if idx < train_count:
            trains.append(val)
        else:
            vals.append(val)

    return trains, vals
