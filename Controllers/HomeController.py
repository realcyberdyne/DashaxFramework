from Reponse.DCookie import DCookieValue
from Reponse.DResponse import DResponse
from Reponse.DView import DView


class HomeController:

    #Get index request
    def index(self, params,request):
        return DResponse(DView("index"))

    def sayhello(self, params,request):
        return DResponse(DView("sayhello",[{"name":"name","value":"Rezafta"}]))