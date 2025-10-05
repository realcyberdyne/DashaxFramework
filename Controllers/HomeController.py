from Reponse.DCookie import DCookieValue
from Reponse.DResponse import DResponse
from Reponse.DView import DView


class HomeController:

    #Get index request
    def index(self, params,request):
        return DResponse(DView("index"))

    def sampleform(self, params,request):
        return DResponse(DView("sample_form"))

    def sayhello(self,request,params):
        return DResponse("Hello %s!" % params["name"])