from Reponse.DResponse import DResponse
from Reponse.DView import DView


class HomeController:

    #Get index request
    def index():
        return DResponse(DView("index"));