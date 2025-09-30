from Reponse.DCookie import DCookieValue
from Reponse.DResponse import DResponse
from Reponse.DView import DView


class HomeController:

    #Get index request
    def index(self, params,request):
        print("Hello ",DCookieValue(request,"name"))
        print("salam ", params.get("name"))
        return DResponse(DView("index"))