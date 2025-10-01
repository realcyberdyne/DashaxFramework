# from Controllers.HomeController import HomeController
#
# class GetMapping:
#
#     @staticmethod
#     def parse_query_string(query_string):
#         result = {}
#
#         # Split by '&' to get individual key-value pairs
#         pairs = query_string.split('&')
#
#         # Process each pair
#         for pair in pairs:
#             if '=' in pair:
#                 key, value = pair.split('=', 1)  # Split only on first '='
#                 result[key] = value
#
#         return result
#
#
#     @staticmethod
#     def MappingHandle(PathAndRequest,request):
#
#         #Request parametrs
#         Parameters = PathAndRequest.split("?")
#
#         #Get Path
#         MainPath =  Parameters[0]
#
#         #Get Parameters
#         params = {}
#         if(len(Parameters) > 1):
#             params = GetMapping.parse_query_string(Parameters[1])
#
#
#         if MainPath == "/":
#             return HomeController().index(params,request)
#         else:
#             return ""
#
#

from Controllers.HomeController import HomeController
import re


class GetMapping:

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
    def parse_path_pattern(pattern, path):
        """
        Match path pattern with actual path and extract parameters
        Example: pattern='/{name}/{family}' and path='/ali/mohammadi'
        Output: {'name': 'ali', 'family': 'mohammadi'}
        """
        # Convert pattern to regex
        # {name} -> (?P<name>[^/]+)
        pattern_regex = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', pattern)
        pattern_regex = '^' + pattern_regex + '$'

        # Match path with pattern
        match = re.match(pattern_regex, path)

        if match:
            return match.groupdict()
        return None

    @staticmethod
    def MappingHandle(PathAndRequest, request):

        # Request parameters
        Parameters = PathAndRequest.split("?")

        # Get Path
        MainPath = Parameters[0]

        # Get Query Parameters
        query_params = {}
        if len(Parameters) > 1:
            query_params = GetMapping.parse_query_string(Parameters[1])

        # Define routes with patterns
        routes = [
            {
                'pattern': '/',
                'controller': HomeController,
                'method': 'index'
            },
            {
                'pattern': '/sayhello',
                'controller': HomeController,
                'method': 'sayhello'
            }
        ]

        # Find matching route
        for route in routes:
            path_params = GetMapping.parse_path_pattern(route['pattern'], MainPath)

            if path_params is not None:
                # Merge query parameters and path parameters
                all_params = {**query_params, **path_params}

                # Call controller method
                controller = route['controller']()
                method = getattr(controller, route['method'])
                return method(all_params, request)

        # If no route found
        return "404 - Not Found"