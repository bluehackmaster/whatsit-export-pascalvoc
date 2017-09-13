import configparser

config = configparser.ConfigParser()
config.read('./config/config.ini')


def getValue(section, value):
    return config[section][value]
