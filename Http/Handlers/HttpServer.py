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


import socket
from concurrent.futures import ThreadPoolExecutor
from Http.Handlers.HttpHandler import HttpHandler


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

    def _handle_connection(self, conn, addr):
        """Handle individual client connection"""
        try:
            print(f'New connection from {addr}')

            # Set socket timeout for this connection
            conn.settimeout(5.0)

            # Receive data with larger buffer
            data = conn.recv(8192)

            if data:
                self._process_request(conn, data)
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
        """Process HTTP request"""
        try:
            request_data = data.decode('utf-8', errors='ignore')
            handler = HttpHandler()
            handler.Requesthandle(request_data, conn)
        except Exception as e:
            print(f"Error processing request: {e}")

    def shutdown(self):
        """Gracefully shutdown the server"""
        print("Shutting down server...")
        self.running = False
        self.executor.shutdown(wait=True)
        try:
            self.socket.close()
        except:
            pass