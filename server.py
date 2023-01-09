import socket
import os


class Server:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(("127.0.0.1", 80))
        self.server_socket.listen()
        self.TIMEOUT_SOCKET = 1
        self.header_ok = "HTTP/1.0 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {file_length}"

    @staticmethod
    def check_msg_get(data):
        check_list = data.split(" ")
        return (check_list[0] == "GET") and ("/" in check_list[1]) and check_list[2] == "HTTP/1.1"

    @staticmethod
    def check_msg_post(data):
        check_list = data.split(" ")
        return (check_list[0] == "POST") and ("/" in check_list[1]) and check_list[2] == "HTTP/1.1"

    def main(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"client {client_address} connected!")
            data = client_socket.recv(1028).decode()
            msg = data
            print(f"{msg = }")
            while len(data) > 0:
                data_request = msg.split("\r\n")[0]

                print(f"data request: {data_request}")
                data_list = data_request.split(" ")
                print(data_list)
                url_data = data_list[1]
                print(f"{url_data =}")
                if self.check_msg_get(data_request):
                    print("Entered trail 1")
                    if url_data == "/":
                        print("Entered door 1")
                        file = open("index.html", "rb").read()
                        content_type = "text/html; charset=utf-8"
                        file_length = len(file)
                        header = self.header_ok.format(content_type=content_type, file_length=file_length)
                        client_socket.send((header + "\r\n\r\n").encode() + file)
                        print("Sent")
                    elif url_data[1::].split("?")[0] == "image":
                        print("Entered to door 2")
                        new_url = url_data.split("=")[1]
                        print(f"{new_url =}")
                        file = open(new_url, "rb").read()
                        content_type = "image/jpeg"
                        file_length = len(file)
                        header = self.header_ok.format(content_type=content_type, file_length=file_length)
                        client_socket.send((header + "\r\n\r\n").encode() + file)
                        print("Sent")
                    elif url_data[1::].split(".")[-1] in ["jpg", "js", "css", "ico", "gif"]:
                        print("Entered door 3")
                        new_url = url_data[1::]
                        file = open(new_url, "rb").read()
                        content_type = new_url.split(".")[-1]
                        if content_type == "jpg":
                            content_type = "image/jpeg"
                        elif content_type == "js":
                            content_type = "text/javascript; charset=UTF-8"
                        elif content_type == "css":
                            content_type = "text/css"
                        elif content_type == "ico":
                            content_type = "image/x-ico"
                        file_length = len(file)
                        header = self.header_ok.format(content_type=content_type, file_length=file_length)
                        client_socket.send((header + "\r\n\r\n").encode() + file)
                        print("Sent")
                    elif url_data[1::].split("?")[0] == "calculate-next":
                        print("Entered door 4")
                        num = str(int(url_data[1::].split("=")[1]) + 1).encode()
                        content_type = "text/plain"
                        file_length = len(file)
                        header = self.header_ok.format(content_type=content_type, file_length=file_length)
                        client_socket.send((header + "\r\n\r\n").encode() + num)
                        print("Sent")
                    elif url_data[1::].split("?")[0] == "calculate-area":
                        print("Entered door 5")
                        height = int(url_data[1::].split("=")[1].split("&")[0])
                        width = int(url_data[1::].split("=")[2])
                        result = str(height * width / 2).encode()
                        content_type = "text/plain"
                        file_length = len(file)
                        header = self.header_ok.format(content_type=content_type, file_length=file_length)
                        client_socket.send((header + "\r\n\r\n").encode() + result)
                        print("Sent")
                    elif not os.path.isfile(url_data[1::]):
                        print("Entered door 6")
                        header = "HTTP/1.0 404 not found"
                        client_socket.send((header + "\r\n\r\n").encode())
                    elif url_data == " " or url_data == "fds.css":
                        print("Entered door 7")
                        header = "HTTP/1.0 403 Forbidden"
                        client_socket.send(header.encode())
                    elif url_data == "page1.html":
                        print("Entered door 8")
                        header = "HTTP/1.0 302 Moved Temporarily\r\npage2.html\r\n"
                        client_socket.send((header + "\r\n\r\n").encode())
                        print("Sent")
                    else:
                        print("Entered door 6")
                        header = "HTTP/1.0 500 Internal Server Error"
                        client_socket.send((header + "\r\n\r\n").encode())
                        print("Sent")
                elif self.check_msg_post(data_request):
                    if url_data[1::].split("?")[0] == "upload":
                        print("Entered to trail2")
                        file_name = url_data.split("=")[1]
                        temp = msg.split("Content-Length:")[1]
                        print(f"{temp =}")
                        file_len = int(temp.split("\r\n")[0])
                        t = b" "
                        image = b""
                        while len(image) < file_len:
                            t = client_socket.recv(1024)
                            image += t
                        content_type = "image/jpeg"
                        print(f"{file_name =}")
                        path = r"C:\Users\yahel\PycharmProjects\pythonProject\webroot"
                        complete_name = os.path.join(path, file_name)
                        print(f"{complete_name =}")
                        with open(complete_name, "wb") as file:
                            file.write(image)
                        header = f"HTTP/1.0 200 OK"
                        to_send_msg = f"{file_name} was copied to {path}"
                        client_socket.send((header + "\r\n\r\n").encode())
                        print("Sent")
                data = client_socket.recv(1024).decode()
                msg += data
            client_socket.close()


if __name__ == "__main__":
    app = Server()
    app.main()
