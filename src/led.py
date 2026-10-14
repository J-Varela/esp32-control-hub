from machine import Pin, PWM

class LEDController:
    def __init__(self, pin=23, frequency=1000):
        self.pwm = PWM(Pin(pin), freq=frequency)
        self.brightness = 0
        self.pwm.duty_u16(0)

    def set_brightness(self, percent):
        if not 0 <= percent <= 100:
            raise ValueError("Brightness must be between 0 and 100")

        duty = round(percent * 65535 / 100)
        self.pwm.duty_u16(duty)
        self.brightness = percent

    def on(self):
        self.set_brightness(100)

    def off(self):
        self.set_brightness(0)

    def get_status(self):
        return {
            "brightness": self.brightness,
            "enabled": self.brightness > 0
        }

    def deinit(self):
        self.pwm.deinit()