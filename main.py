from machine import Pin, PWM
import lcd
import time
import os
import machine
from display_utils import read_bmp_to_buffer
from wifi_utils import wlan_connect

BL = 13

if __name__ == "__main__":

    wlan = wlan_connect()

    try:
        # Set up the LCD
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)  # max 65535

        lcd_display = lcd.LCD_1inch8()

        # Display a loading screen
        lcd_display.fill(lcd_display.BLACK)
        lcd_display.text("Loading...", 2, 28, lcd_display.WHITE)

        lcd_display.show()

        # Iterate through showing all the BMP images in the images directory
        images = os.listdir("images")
        while True:
            for image_filename in sorted(images):
                image_path = "images/" + image_filename
                print("Loading " + image_path)

                # Load the image from the file and write it to the LCD buffer
                lcd_display.fill(0x0000)
                with open(image_path, "rb") as input_stream:
                    read_bmp_to_buffer(lcd_display, input_stream)

                print("Loaded")

                # Show the image on the display
                lcd_display.show()

                # Wait a bit before trying to load the next image. Actual time till next image shows is a
                # few seconds more due to time to load next image from flash storage.
                sensor_temp = machine.ADC(4)
                conversion_factor = 3.3 / 65535
                reading = (sensor_temp.read_u16() * conversion_factor)
                temperature = 27 - (reading - 0.706)/0.001721
                print("Temperature "+str(temperature))
                time.sleep(5)

    except KeyboardInterrupt as e:
        wlan_disconnect()
