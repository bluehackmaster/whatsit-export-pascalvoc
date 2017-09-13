import os
from util import Comm

PROJECT_NAME = 'FOODS'
DATASETS = ['sushi', 'tofu_soup', 'fried_chicken', 'pizza']
IMAGE = ['image1.jpg', 'image2.jpg']
PROJECT_PATH = Comm.makeProjectDirectory(PROJECT_NAME)
Comm.makeDatasetDirectory(PROJECT_NAME, DATASETS)

# Creating a 'label_map.pbtxt' file
Comm.writeFile(os.path.join(PROJECT_PATH, 'data/label_map.pbtxt'), Comm.makelabelMap(DATASETS))

for dataset in DATASETS:
    for image in IMAGE:
        Comm.writeFile(os.path.join(PROJECT_PATH, 'dataset/' + dataset + '/Annotations/' + image + '.xml'),
                       Comm.makeImageData(dataset, image, DATASETS))
