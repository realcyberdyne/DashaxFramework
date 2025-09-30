from Reponse.DResponse import DResponse
from Route import FileManagerMapping
from Route.AssetMapping import AssetMapping
from Route.GetMapping import GetMapping
from Route.RepositoryMapping import RepositoryMapping


class HttpHandler:

    def Requesthandle(self, request,response):

        RequestData = self.GetRequestAddressTypeAnd(request)
        FinalResponse = DResponse("")

        if str(RequestData[0]).upper()=="GET":
            if "ASSETS" in RequestData[1].upper():
                FinalResponse = AssetMapping.MappingHandle(RequestData[1],request)
            elif "Files" in RequestData[1].upper():
                FinalResponse = RepositoryMapping.MappingHandle(RequestData[1],request)
            elif "FileManager" in RequestData[1].upper():
                FinalResponse = FileManagerMapping.MappingHandle(RequestData[1],request)
            else:
                FinalResponse = GetMapping.MappingHandle(RequestData[1],request)


        #Get Check response type
        if isinstance(FinalResponse, DResponse):
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