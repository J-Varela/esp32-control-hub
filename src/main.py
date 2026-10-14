
from led import LEDController
from wifi import connect_wifi
from server import start_server
from config import WIFI_SSID, WIFI_PASSWORD


def main():
    print("Starting ESP32 Control Hub...")

    led = LEDController(pin=23)

    try:
        wifi = connect_wifi(
            WIFI_SSID,
            WIFI_PASSWORD
        )

        ip = wifi.ifconfig()[0]

        print("Device ready!")
        print("Status API: http://" + ip + "/api/status")

        start_server(led)

    finally:
        led.off()
        led.deinit()


if __name__ == "__main__":
    main()
