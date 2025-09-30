import mimetypes
import os

class RepositoryMapping:
    def MappingHandle(PathAndRequest):

        current_dir = os.getcwd()
        asset_file = current_dir + "/Files" + PathAndRequest.upper().split("/Files")[1]

        content_type, _ = mimetypes.guess_type(asset_file)
        content_type = content_type or 'application/octet-stream'

        with open(asset_file, 'rb') as f:
            file_data = f.read()

        response_header = (
            'HTTP/1.1 200 OK\r\n'
            f'Content-Type: {content_type}\r\n'
            f'Content-Length: {len(file_data)}\r\n'
            'Connection: close\r\n'
            '\r\n'
        )
        return response_header.encode() + file_data




