from machine import Pin, PWM
import lcd
import time
import gc
import json
import uasyncio
from urllib.urequest import urlopen
from display_utils import read_bmp_to_buffer
from wifi_utils import wlan_connect, wlan_disconnect

BL = 13
button = Pin(16, Pin.IN, Pin.PULL_UP)


async def display_images(image_list):

    while True:
        for image in image_list:
            print("Loading " + image["key"])

            lcd_display.fill(0x0000)

            with open(image["key"], "rb") as input_stream:
                read_bmp_to_buffer(lcd_display, input_stream)

            print("Loaded")

            lcd_display.show()

            now = time.time()
            flag = False
            while time.time() < now + 2:
                await uasyncio.sleep_ms(10)
                if not flag and not button.value():
                    print("Button Pressed")
                    flag = True


async def main():
    await uasyncio.create_task(display_images(image_list))
    await uasyncio.sleep_ms(10000)


if __name__ == "__main__":

    wlan = wlan_connect()

    try:
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)  # max 65535

        lcd_display = lcd.LCD_1inch8()

        lcd_display.fill(lcd_display.BLACK)
        lcd_display.text("Loading...", 2, 28, lcd_display.WHITE)

        lcd_display.show()

        r = urlopen("https://d3pkoikmm0xava.cloudfront.net/list/list.json")
        image_list = json.loads(r.read())
        r.close()
        print(f'Image list:\n{image_list}')

        gc.collect()
        print(f'Free memory: {gc.mem_free()}')

        print('Downloading images')
        for image in image_list:
            gc.collect()
            print(f'Reading {image["key"]}')
            print(f'Free memory: {gc.mem_free()}')
            r = urlopen(f'https://d3pkoikmm0xava.cloudfront.net/images/{image["key"]}')

            with open(image["key"], 'wb') as fd:
                fd.write(r.read())
                r.close()
            print('Done')

        wlan_disconnect()
        print('Displaying images')
        uasyncio.run(main())

    except KeyboardInterrupt as e:
        wlan_disconnect()


