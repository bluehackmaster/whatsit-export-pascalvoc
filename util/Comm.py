import os
import shutil
from . import Config
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET

CONFIG_TEMP_PATH = Config.getValue('FILE', 'TEMP_PATH')


# TODO : Convert to class from this logic for saving project name(to reuse).

# noinspection PyPep8Naming
def checkAndCreateDirectory(paths):
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)


def makeProjectDirectory(project):
    PROJECT_TEMP_PATH = os.path.join(CONFIG_TEMP_PATH, project)
    folders = ['data', 'models', 'models/model', 'models/model/eval', 'models/model/train', 'dataset']

    checkAndCreateDirectory([CONFIG_TEMP_PATH, PROJECT_TEMP_PATH])

    for folder in folders:
        os.mkdir(os.path.join(PROJECT_TEMP_PATH, folder))

    return PROJECT_TEMP_PATH


def makeDatasetDirectory(project, datasets):
    PROJECT_TEMP_PATH = os.path.join(CONFIG_TEMP_PATH, project)

    for dataset in datasets:
        folders = ['dataset/' + dataset, 'dataset/' + dataset + '/Annotations',
                   'dataset/' + dataset + '/JPEGImages', 'dataset/' + dataset + '/ImageSets',
                   'dataset/' + dataset + '/ImageSets/Main']

        for folder in folders:
            os.mkdir(os.path.join(PROJECT_TEMP_PATH, folder))


def writeFile(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


def makelabelMap(labels):
    rslt = ''

    for idx, val in enumerate(labels):
        rslt += 'item { \n id: ' + str(idx + 1) + '\n name: \'' + val + '\'\n}\n\n'

    return rslt.encode('utf-8')

def makeImageData(dataset, image, objects):
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
        annotation.append(makeImageObject(idx))

    return ET.tostring(annotation, encoding='UTF-8', method='xml')


def makeImageObject(abc):
    object = Element('object')

    SubElement(object, 'name').text = 'bicycle'+str(abc)
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






