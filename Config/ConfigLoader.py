import json

HOST = '127.0.0.1'
PORT = 8080

class ConfigLoader:
    def __init__(self, configFilePath):
        with open(configFilePath, 'r') as f:
            config = json.load(f)

            ConfigLoader.HOST = config['app']['HOST']
            ConfigLoader.PORT = config['app']['PORT']


