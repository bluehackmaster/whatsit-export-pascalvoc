import os

from util.Pascal import Pascal

pascal = Pascal(os.path.join(os.path.join(os.path.dirname(__file__), 'tmp')), '59b686a6adc71eb86c669725')
pascal.execute()
