import json

from werkzeug.exceptions import RequestTimeout

HOST = '127.0.0.1'
PORT = 8080
BUFFERSIZE = 8192
RequestTimeout = 0.5
MAX_FILE_SIZE = 1024 * 1024 * 10
UPLOAD_DIR = "C:\\Users\\rezafta\\Desktop\\DashaxFramework\\FileTmp"

class ConfigLoader:
    def __init__(self, configFilePath):
        with open(configFilePath, 'r') as f:
            config = json.load(f)

            ConfigLoader.HOST = config['app']['HOST']
            ConfigLoader.PORT = config['app']['PORT']
            ConfigLoader.BUFFERSIZE = config['app']['BUFFERSIZE']
            ConfigLoader.RequestTimeout = config['app']['RequestTimeOut']
            ConfigLoader.MAX_FILE_SIZE = 1024 * 1024 * int(config['app']['MAX_FILE_SIZE'])
            ConfigLoader.UPLOAD_DIR = config['app']['UPLOAD_DIR']


