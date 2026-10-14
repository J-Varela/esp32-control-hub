import network
from time import sleep


def connect_wifi(ssid, password, timeout=20):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        wifi.connect(ssid, password)

        for _ in range(timeout):
            if wifi.isconnected():
                break
            sleep(1)

    if not wifi.isconnected():
        raise RuntimeError("Wi-Fi connection failed")

    print("Wi-Fi connected!")
    print("IP address:", wifi.ifconfig()[0])

    return wifi