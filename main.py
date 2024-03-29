from machine import Pin
import lcd
import gc
import json
import uasyncio
import lowpower
import os
from urllib.urequest import urlopen
from display_utils import read_bmp_to_buffer
from wifi_utils import wlan_connect, wlan_disconnect

button = Pin(16, Pin.IN, Pin.PULL_UP)
DORMANT_PIN = 15


async def display_images(image_list):
    while True:
        for image in image_list:
            print("Loading " + image["key"])

            with open(image["key"], "rb") as input_stream:
                await read_bmp_to_buffer(lcd_display, input_stream)

            print("Loaded")

            lcd_display.show()

            await uasyncio.sleep(2)


async def cancel_button():
    while True:
        await uasyncio.sleep(0)
        if not button.value():
            break
    return True


async def main():
    display_images_task = uasyncio.create_task(display_images(image_list))
    try:
        await uasyncio.wait_for(cancel_button(), 180)
    except uasyncio.TimeoutError:
        print("TIMEOUT")

    print("CANCELLING...")
    display_images_task.cancel()
    print("CANCELLED")


if __name__ == "__main__":

    lcd_display = lcd.LCD_1inch8()
    try:
        lcd_display.set_brightness(60)

        lcd_display.fill(lcd_display.BLACK)
        lcd_display.text("Initialising...", 2, 28, lcd_display.WHITE)
        lcd_display.show()

        for file in os.listdir("/"):
            if file.endswith(".bmp"):
                print(f"Deleting {file}")
                os.remove(file)
                print(f"Deleted {file}")

        print("Confirming...")
        for file in os.listdir("/"):
            if file.endswith(".bmp"):
                print(f"Deleting {file}")
                os.remove(file)
                print(f"Deleted {file}")


        lcd_display.fill(lcd_display.BLACK)
        lcd_display.text("Connecting...", 2, 28, lcd_display.WHITE)
        lcd_display.show()

        wlan = wlan_connect()

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
                gc.collect()
                fd.write(r.read())
                r.close()
                fd.close()
            print('Done')

        wlan_disconnect()
        print('Displaying images')
        uasyncio.run(main())
        print('STOPPING')

        # turn off display
        print("POWERING DOWN")
        lcd_display.set_brightness(0)
        print("DISPLAY OFF")
        wlan_disconnect()
        print("WLAN OFF")
        print("GOING DORMANT")
        lowpower.dormant_until_pin(DORMANT_PIN)
        print("OUT OF DORMANT")

    except KeyboardInterrupt as e:
        print('INTERRUPTED')
        gc.collect()
        print(f'Free memory: {gc.mem_free()}')

        lcd_display.set_brightness(60)
        lcd_display.fill(lcd_display.BLACK)
        lcd_display.text("INTERRUPTED", 2, 28, lcd_display.WHITE)
        lcd_display.show()
