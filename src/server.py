
import json
import socket

from api import handle_request


def read_request(client):
    client.settimeout(5)

    data = b""

    while b"\r\n\r\n" not in data:
        chunk = client.recv(1024)

        if not chunk:
            raise ValueError("Incomplete HTTP headers")

        data += chunk

        if len(data) > 4096:
            raise ValueError("HTTP headers too large")

    header_bytes, body = data.split(b"\r\n\r\n", 1)
    lines = header_bytes.decode().split("\r\n")

    request_line = lines[0].split()

    if len(request_line) != 3:
        raise ValueError("Invalid HTTP request line")

    method, path, version = request_line

    content_length = 0

    for line in lines[1:]:
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())

    if content_length < 0 or content_length > 1024:
        raise ValueError("Invalid request body size")

    while len(body) < content_length:
        chunk = client.recv(
            min(1024, content_length - len(body))
        )

        if not chunk:
            raise ValueError("Incomplete request body")

        body += chunk

    return method, path.split("?")[0], body[:content_length].decode()


def start_server(led, port=80, telemetry=None):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(("0.0.0.0", port))
        server.listen(2)
        server.settimeout(2)

        print("HTTP server running on port", port)

        while True:
            try:
                client, address = server.accept()

            except OSError as error:
                # A timeout is expected when nobody connects.
                if error.args and error.args[0] in (110, 116):
                    continue

                print("Socket accept error:", error)
                raise

            try:
                method, path, request_body = read_request(client)
                status_code, result = handle_request(
                    method,
                    path,
                    request_body,
                    led,
                    telemetry
                )
                body = json.dumps(result)
                status_text = {
                    200: "OK",
                    400: "Bad Request",
                    404: "Not Found",
                    503: "Service Unavailable"
                }.get(status_code, "Error")
                response = (
                    "HTTP/1.1 {} {}\r\n"
                    "Content-Type: application/json\r\n"
                    "Content-Length: {}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                ).format(
                    status_code,
                    status_text,
                    len(body.encode())
                )
                client.sendall(response.encode())
                client.sendall(body.encode())

            except (OSError, ValueError, UnicodeError) as error:
                print("Client error:", error)

            finally:
                client.close()

    finally:
        server.close()
        print("HTTP server closed")
