from Controllers.HomeController import HomeController
from Http.Middleware.MainMiddleWare import MainMiddleware


class PostMapping:

    @staticmethod
    def parse_query_string(query_string):
        result = {}

        # Split by '&' to get individual key-value pairs
        pairs = query_string.split('&')

        # Process each pair
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)  # Split only on first '='
                result[key] = value

        return result


    @staticmethod
    def MappingHandle(PathAndRequest,request):

        #Request parametrs
        Parameters = PathAndRequest.split("?")

        #Get Path
        MainPath =  Parameters[0]

        #Get Parameters
        params = {}
        if(len(Parameters) > 1):
            params = PostMapping.parse_query_string(Parameters[1])


        if MainPath == "/":
            return HomeController().index(params, request)

            #Smaple middleware use
            # return HomeController().index(params, request) if MainMiddleware(request) else "OK"
        else:
            return ""


