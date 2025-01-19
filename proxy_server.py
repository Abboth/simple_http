import saver
import socket
import logging


def echo_server(host: str, port: int) -> None:
    sock = socket.socket()

    server = host, port
    sock.bind(server)
    sock.listen()
    conn, addr = sock.accept()

    logging.info(f"Echo Server started on {host}:{port}")
    try:
        while True:
            data = conn.recv(1024)
            parsed_data = saver.saver_to_json(data)
            logging.info(f"Received POST request: {parsed_data}")
            msg = input(">>> ")
            conn.send(msg.encode())
            sock.sendto(data, addr)

    except KeyboardInterrupt:
        logging.info(f"Echo Server stopped")
    finally:
        sock.close()
