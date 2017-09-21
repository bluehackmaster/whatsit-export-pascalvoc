import os

from util.Pascal import Pascal

print(os.environ)

__project_id = None

try:
    __project_id = os.environ['PROJECT_ID'].replace('"', '')
except Exception as ex:
    print('Not defined project ID value::')
    print(ex)

print('Project Id::' + __project_id)

pascal = Pascal(os.path.join(os.path.join(os.path.dirname(__file__), 'tmp')), __project_id)
pascal.execute()
