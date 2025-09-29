from Config.ConfigLoader import ConfigLoader
from Http.HttpServer import HTTPServer

def main():
    # Store the ConfigLoader instance
    config_loader = ConfigLoader('config.json')

    # Use instance attributes
    HTTPServer(config_loader.PORT,config_loader.HOST)



if __name__ == '__main__':
    main()