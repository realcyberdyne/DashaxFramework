import socket
import threading
from Http.HttpHandler import HttpHandler


class HTTPServer:
    def __init__(self, PORT,host):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as HttpSocket:
            HttpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
            HttpSocket.bind((host, PORT))
            HttpSocket.listen()

            #Get Show user
            print("DashaxFramework http server started on port " + str(PORT))

            while True:  # Added loop to handle multiple connections
                conn, addr = HttpSocket.accept()
                with conn:
                    print('New Connection From ', addr)
                    data = conn.recv(1024)
                    # threading.Thread(target=self.Requesthandle,args=(conn,data)).start()
                    self.Requesthandle(conn,data)


    def Requesthandle(self,conn,data):
        if data:
            # print(f"Received: {data.decode()}")
            request_data = data.decode('utf-8')
            handler = HttpHandler()
            handler.Requesthandle(request_data, conn)