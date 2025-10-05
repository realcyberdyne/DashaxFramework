from Controllers.HomeController import HomeController
from Http.Middleware.MainMiddleWare import MainMiddleware
import re
from typing import Dict, Any

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
    def extract_form_data(raw_request: str) -> Dict[str, Any]:
        form_data = {}

        # Find boundary from Content-Type
        boundary_match = re.search(r'WebKitFormBoundary\w+', raw_request)
        if not boundary_match:
            return form_data

        boundary = boundary_match.group(0)

        # Split request into different parts
        parts = raw_request.split(f'------{boundary}')

        for part in parts:
            if not part.strip() or part.strip() == '--':
                continue

            # Extract field name
            name_match = re.search(r'name="([^"]+)"', part)
            if name_match:
                field_name = name_match.group(1)

                # Check if it's a file or not
                filename_match = re.search(r'filename="([^"]+)"', part)

                if filename_match:
                    # If it's a file
                    filename = filename_match.group(1)
                    content_type_match = re.search(r'Content-Type:\s*([^\r\n]+)', part)
                    content_type = content_type_match.group(1) if content_type_match else 'unknown'

                    form_data[field_name] = {
                        'type': 'file',
                        'filename': filename,
                        'content_type': content_type
                    }
                else:
                    # If it's a text field
                    # Split by double line break to separate headers from content
                    parts_split = re.split(r'\r?\n\r?\n', part, maxsplit=1)
                    if len(parts_split) > 1:
                        value = parts_split[1].strip()
                    else:
                        value = ''

                    form_data[field_name] = value

        return form_data

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

        input_params = request.split("\r\n\r\n")
        if(len(input_params) <= 0):
            input_params = request.split("\n\n")

        params = PostMapping.extract_form_data(request)

        if params == {}:
            params = PostMapping.parse_query_string(input_params[1])

        print(params)



        if MainPath == "/":
            return HomeController().index(params, request)

            #Smaple middleware use
            # return HomeController().index(params, request) if MainMiddleware(request) else "OK"
        elif MainPath == "/sampleform":
            return HomeController().sayhello(request,params)
        else:
            return ""

