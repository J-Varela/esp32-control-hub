
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from server import read_request


class FakeClient:
    def __init__(self, chunks):
        self.chunks = iter(chunks)

    def settimeout(self, timeout):
        self.timeout = timeout

    def recv(self, size):
        return next(self.chunks, b"")


def test_read_get_request():
    client = FakeClient([
        b"GET /api/status HTTP/1.1\r\n"
        b"Host: esp32\r\n\r\n"
    ])

    method, path, body = read_request(client)

    assert method == "GET"
    assert path == "/api/status"
    assert body == ""


def test_read_post_request_in_chunks():
    client = FakeClient([
        b"POST /api/led HTTP/1.1\r\n"
        b"Content-Length: 18\r\n\r\n"
        b'{"bright',
        b'ness": 50}'
    ])

    method, path, body = read_request(client)

    assert method == "POST"
    assert path == "/api/led"
    assert body == '{"brightness": 50}'
