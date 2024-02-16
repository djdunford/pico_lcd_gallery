from machine import Pin
import lcd
import gc
import json
import uasyncio
from urllib.urequest import urlopen
from display_utils import read_bmp_to_buffer
from wifi_utils import wlan_connect, wlan_disconnect

button = Pin(16, Pin.IN, Pin.PULL_UP)


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

    wlan = wlan_connect()

    try:
        lcd_display = lcd.LCD_1inch8()
        lcd_display.set_brightness(60)

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
        print('Stopping')

    except KeyboardInterrupt as e:
        print('INTERRUPTED')
        gc.collect()
        print(f'Free memory: {gc.mem_free()}')

    # turn off display
    print("TURNING DISPLAY OFF")
    lcd_display.off()
    print("DISPLAY OFF")
    # await uasyncio.wait_for(cancel_button(), 20)
    # lcd_display.on()

    wlan_disconnect()
