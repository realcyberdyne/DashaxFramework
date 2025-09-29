from Controllers.HomeController import HomeController


class GetMapping:
    def MappingHandle(PathAndRequest):
        if PathAndRequest == "/":
            return HomeController.index()
        else:
            return ""



