import socket


class App:
    def __init__(self, host: str, port: int):
        self.SERVER_HOST = host
        self.SERVER_PORT = port

    def run(self):
        # socket host
        # SERVER_HOST = "0.0.0.0"
        # SERVER_PORT = 8080

        # making the socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        server_socket.listen(1)
        print(f"listening on port: {self.SERVER_PORT}")

        while True:
            # wait for client connection
            client_connection, client_address = server_socket.accept()

            # get client request
            request = client_connection.recv(1024).decode()
            print(f"request: {request}")

            # parse HTTP headers
            headers = request.split("\n")
            file_name = headers[0].split()[1]
            print(f"file name: {file_name}")

            # get contents of the file
            if file_name == "/":
                file_name = "/index.html"
            else:
                file_name = f"/{file_name}.html"
            file_name = "Views" + file_name

            try:
                fin = open(file_name)
                content = fin.read()
                fin.close()
            except FileNotFoundError:
                response = "HTTP/1.0 404 NOT FOUND\n\nFile Not Found"

            # send http response
            response = f"HTTP/1.0 200 OK\n\n {content}"
            client_connection.sendall(response.encode())
            client_connection.close()

        # close the socket
        server_socket.close()
