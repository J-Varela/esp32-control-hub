
import json
import socket
import time



def start_server(led, port=80):
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
                request = client.recv(1024).decode()
                parts = request.split()

                if len(parts) < 2:
                    continue

                method = parts[0]
                path = parts[1].split("?")[0]

                if method == "GET" and path == "/api/status":
                    body = json.dumps({
                        "device": "ESP32 Control Hub",
                        "led": led.get_status()
                    })
                    status = "200 OK"

                else:
                    body = json.dumps({
                        "error": "Not found"
                    })
                    status = "404 Not Found"

                response = (
                    "HTTP/1.1 " + status + "\r\n"
                    "Content-Type: application/json\r\n"
                    "Connection: close\r\n\r\n"
                    + body
                )

                client.sendall(response.encode())

            except OSError as error:
                print("Client error:", error)

            finally:
                client.close()

    finally:
        server.close()
        print("HTTP server closed")
