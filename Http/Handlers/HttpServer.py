# import socket
# import threading
# from Http.HttpHandler import HttpHandler
#
#
# class HTTPServer:
#     def __init__(self, PORT,host):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as HttpSocket:
#             HttpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
#             HttpSocket.bind((host, PORT))
#             HttpSocket.listen()
#
#             #Get Show user
#             print("DashaxFramework http server started on port " + str(PORT))
#
#             while True:  # Added loop to handle multiple connections
#                 conn, addr = HttpSocket.accept()
#                 with conn:
#                     print('New Connection From ', addr)
#                     data = conn.recv(1024)
#                     # threading.Thread(target=self.Requesthandle,args=(conn,data)).start()
#                     self.Requesthandle(conn,data)
#
#
#     def Requesthandle(self,conn,data):
#         if data:
#             # print(f"Received: {data.decode()}")
#             request_data = data.decode('utf-8')
#             handler = HttpHandler()
#             handler.Requesthandle(request_data, conn)
import os
import socket
from concurrent.futures import ThreadPoolExecutor
import re

import Config.ConfigLoader
from Http.Handlers.HttpHandler import HttpHandler
from Reponse.DRequest import DRequest


class HTTPServer:
    def __init__(self, port, host, max_workers=10):
        self.port = port
        self.host = host
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = True

        # Create socket outside context manager for proper lifecycle control
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle's algorithm
        self.socket.settimeout(1.0)  # Allow periodic checks for shutdown

        try:
            self.socket.bind((host, port))
            self.socket.listen(128)  # Increased backlog for better throughput

            print(f"DashaxFramework HTTP server started on {host}:{port}")
            self._accept_connections()
        except Exception as e:
            print(f"Server error: {e}")
            self.shutdown()

    def _accept_connections(self):
        """Main loop to accept incoming connections"""
        while self.running:
            try:
                conn, addr = self.socket.accept()
                # Submit connection handling to thread pool
                self.executor.submit(self._handle_connection, conn, addr)
            except socket.timeout:
                continue  # Check if server should still be running
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")


    # def _handle_connection(self, conn, addr):
    #     try:
    #         print(f'New connection from {addr}')
    #
    #         # Set socket timeout for this connection
    #         conn.settimeout(Config.ConfigLoader.RequestTimeout)
    #
    #         # Receive data with larger buffer
    #         data = conn.recv(Config.ConfigLoader.BUFFERSIZE)
    #
    #         print("Split 1 ",data.decode('utf-8', errors='ignore'))
    #         print("-------------------------------------")
    #
    #         #Check file upload
    #         if ("Content-Length:" in str(data)):
    #             Content_Length = DRequest(data.decode('utf-8', errors='ignore'), "Content-Length")
    #             # Boundary = list(DRequest(data.decode('utf-8', errors='ignore'), "Content-Type").encode("utf-8"))
    #
    #             print("c l :", str(Content_Length))
    #             UploadData = bytes()
    #             FileCouunter=0
    #             while True:
    #                 try:
    #                     chunk = conn.recv(int(Content_Length))
    #                     UploadData = UploadData + chunk
    #                 except Exception as e:
    #                     if(FileCouunter <= 1):
    #                         break
    #                     FileCouunter=1
    #
    #             UploadData = UploadData[:-46]
    #
    #
    #             print("Split 2 :", UploadData.decode('utf-8', errors='ignore'))
    #
    #             Content_Dispositions = DRequest(UploadData.decode('utf-8', errors='ignore'), "Content-Disposition")
    #             for Content_Disposition in Content_Dispositions:
    #                 if "filename=" in Content_Disposition:
    #                     Content_Disposition = Content_Disposition.split(";")[2]
    #                     file_name = Content_Disposition.split('="')[1].split('"')[0].strip()
    #                     print("name is : ", file_name)
    #                     print("-------------------------------------")
    #                     index = -1
    #                     for i, byte in enumerate(UploadData):
    #                         if byte == 0xFF:
    #                             index = i
    #                             break
    #
    #                     if index != -1 and index + 1 < len(UploadData):
    #                         remaining_data = UploadData[index + 1:]
    #                         print("Split:", remaining_data.decode('utf-8', errors='ignore'))
    #
    #                         # Get create file in temp file
    #                         current_dir = os.getcwd()
    #                         mode = 'ab' if os.path.exists(current_dir + "/FileTmp/" + file_name) else 'wb'
    #                         with open(current_dir + "/FileTmp/" + file_name, mode) as f:
    #                             f.write(remaining_data)
    #                     else:
    #                         break
    #                         print("Not Found")
    #
    #
    #         if data:
    #             self._process_request(conn, data)
    #     except socket.timeout:
    #         print(f"Connection timeout from {addr}")
    #     except Exception as e:
    #         print(f"Error handling connection from {addr}: {e}")
    #     finally:
    #         try:
    #             conn.close()
    #         except:
    #             pass

    @staticmethod
    def _parse_multipart(body, boundary):
        boundary = b'--' + boundary.encode('utf-8')
        parts = body.split(boundary)
        for part in parts[1:-1]:  # Skip first (empty) and last (--boundary--)
            if b'Content-Disposition' in part and b'filename=' in part:
                # Remove leading \r\n
                part = part.lstrip(b'\r\n')
                headers_end = part.find(b'\r\n\r\n')
                if headers_end == -1:
                    continue
                headers = part[:headers_end].decode('utf-8', errors='ignore')
                content = part[headers_end + 4:]
                # Extract filename from Content-Disposition
                match = re.search(r'filename="([^"]+)"', headers)
                if match:
                    filename = match.group(1)
                    # Remove trailing \r\n if present
                    content = content.rstrip(b'\r\n')
                    return filename, content
        return None, None

    def _handle_connection(self, conn, addr):
        try:
            # print(f'New connection from {addr}')
            conn.settimeout(Config.ConfigLoader.RequestTimeout)

            # Receive data until we have the full headers
            data = b''
            while True:
                chunk = conn.recv(Config.ConfigLoader.BUFFERSIZE)
                if not chunk:
                    return
                data += chunk
                if b'\r\n\r\n' in data:
                    break

            # Split headers and initial body
            headers_end = data.find(b'\r\n\r\n')
            headers_str = data[:headers_end].decode('utf-8', errors='ignore')
            body = data[headers_end + 4:]

            # print("Received headers:", headers_str)

            # Parse headers for Content-Type and Content-Length
            content_type_match = re.search(r'Content-Type: multipart/form-data; boundary=([^\r\n;]+)', headers_str,
                                           re.IGNORECASE)
            content_length_match = re.search(r'Content-Length: (\d+)', headers_str, re.IGNORECASE)

            if content_type_match and content_length_match:
                boundary = content_type_match.group(1).strip()
                content_length = int(content_length_match.group(1))

                if content_length > Config.ConfigLoader.MAX_FILE_SIZE:
                    # print(f"File too large from {addr}: {content_length} bytes")
                    return

                # Receive remaining body
                bytes_remaining = content_length - len(body)
                while bytes_remaining > 0:
                    chunk = conn.recv(min(bytes_remaining, Config.ConfigLoader.BUFFERSIZE))
                    if not chunk:
                        break
                    body += chunk
                    bytes_remaining -= len(chunk)

                # Ensure we received all data
                if len(body) < content_length:
                    # print(f"Incomplete data received from {addr}: {len(body)}/{content_length}")
                    return

                # Parse multipart body
                filename, file_content = self._parse_multipart(body, boundary)
                if filename and file_content:
                    # Sanitize filename to prevent directory traversal
                    filename = os.path.basename(filename.strip())
                    if not filename:
                        print(f"Invalid filename from {addr}")
                        return

                    # Save file
                    upload_dir = Config.ConfigLoader.UPLOAD_DIR
                    os.makedirs(upload_dir, exist_ok=True)
                    file_path = os.path.join(upload_dir, filename)

                    with open(file_path, 'wb') as f:
                        f.write(file_content)


            # Handle non-upload requests
            full_data = data
            self._process_request(conn, full_data)

        except socket.timeout:
            print(f"Connection timeout from {addr}")
        except Exception as e:
            print(f"Error handling connection from {addr}: {e}")
        finally:
            try:
                conn.close()
            except:
                pass


    def _process_request(self, conn, data):
        try:
            request_data = data.decode('utf-8', errors='ignore')
            handler = HttpHandler()
            handler.Requesthandle(request_data, conn)
        except Exception as e:
            print(f"Error processing request: {e}")

    def shutdown(self):
        print("Shutting down server...")
        self.running = False
        self.executor.shutdown(wait=True)
        try:
            self.socket.close()
        except:
            pass