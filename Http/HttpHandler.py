from Reponse.Response import Response
from Route.AssetMapping import AssetMapping
from Route.GetMapping import GetMapping


class HttpHandler:

    def Requesthandle(self, request,response):

        RequestData = self.GetRequestAddressTypeAnd(request)
        FinalResponse = Response("");

        if str(RequestData[0]).upper()=="GET":
            if "ASSETS" in RequestData[1].upper():
                FinalResponse = AssetMapping.MappingHandle(RequestData[1])
            else:
                FinalResponse = GetMapping.MappingHandle(RequestData[1])

        if isinstance(FinalResponse, Response):
            try:
                if FinalResponse.content_type is not None:
                    if FinalResponse.content_type == "text/html":
                        response.sendall(("HTTP/1.1 " + str(
                            FinalResponse.status_code) + " \r\nContent-Type: " + FinalResponse.content_type + "\r\n\r\n" + FinalResponse.content).encode())
                    else:
                        response.sendall((
                                                     "HTTP/1.1 404 Not Found\r\nContent-Type: " + FinalResponse.content_type + "\r\n\r\n" + "Not Found").encode())
            except Exception as e:
                print(e)
                response.sendall((
                                         "HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n" + "Not Found").encode())
        else:
            if isinstance(FinalResponse, bytes):
                response.sendall(FinalResponse)
            elif isinstance(FinalResponse, str):
                response.sendall(FinalResponse.encode())
            else:
                response.sendall((
                                         "HTTP/1.1 500 Internal Server Error\r\nContent-Type:text/html\r\n\r\n" + "Invalid Response Type").encode())

    def GetRequestAddressTypeAnd(self, request):
        FirstLine = request.split('\n')[0]
        FirstLineData = FirstLine.split(' ')
        RequestType = FirstLineData[0]
        RequestAddress = FirstLineData[1]
        RequestProtocol = FirstLineData[2]

        return RequestType, RequestAddress, RequestProtocol