import os

from util.Pascal import Pascal

pascal = Pascal(os.path.join(os.path.join(os.path.dirname(__file__), 'tmp')))
pascal.execute()
