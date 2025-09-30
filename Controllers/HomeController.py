from Reponse.DCookie import DCookieValue
from Reponse.DResponse import DResponse
from Reponse.DView import DView


class HomeController:

    #Get index request
    def index(self, request):
        print("Hello ",DCookieValue(request,"name"))
        return DResponse(DView("index"))