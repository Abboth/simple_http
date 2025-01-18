from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from pathlib import Path
from storage.saver import saver_to_json
import urllib.parse
import mimetypes
import logging
import socket

BASE_DIR = Path()
HTTP_PORT = 3000
HTTP_HOST = "0.0.0.0"
SOCKET_PORT = 5000
SOCKET_HOST = "localhost"
BUFFER_SIZE = 1024


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html_file("index.html")
            case "/message":
                self.send_html_file("message.html")
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static()
                else:
                    self.send_html_file("error.html", status=404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        client_socket.close()

        self.send_response(200)
        self.send_header("Location", "/contact")
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open(filename, "r") as f:
            self.wfile.write(f.read().encode())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-Type", mt[0])
        else:
            self.send_header("Content-Type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def up_http(host, port):
    address = (host, port)
    server = HTTPServer(address, HttpHandler)  # type: ignore
    logging.info(f"HTTP server started at {address}")
    try:
        server.serve_forever()
    except KeyboardInterrupt as e:
        server.server_close()
        logging.error(f"error while serving: {e}")


def up_socket(host: str, port: int) -> None:
    address = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)
    logging.info(f"Socket server started at {address}")
    try:
        while True:
            msg, addr = sock.recvfrom(BUFFER_SIZE)
            saver_to_json(msg.decode())

    except KeyboardInterrupt as e:
        sock.close()
        logging.error(f"error while serving: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    th_socket = Thread(target=up_socket, args=(SOCKET_HOST, SOCKET_PORT))
    th_http = Thread(target=up_http, args=(HTTP_HOST, HTTP_PORT))
    th_socket.start()
    th_http.start()
