from machine import Pin,SPI,PWM
import lcd
import framebuf
import time
import utime
import random
import math
import os
import bmp_file_reader as bmpr

BL = 13


def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour
    
def ring(cx,cy,r,cc):   # Centre (x,y), radius
    for angle in range(0, 90, 2):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        LCD.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        LCD.pixel(cx-x3,cy-y3,cc)
        LCD.pixel(cx+x3,cy+y3,cc)
        LCD.pixel(cx+x3,cy-y3,cc)
        
def to_color(red, green, blue):
    brightness = 1.0

    # Convert from 8-bit colors for red, green, and blue to 5-bit for blue and red and 6-bit for green.
    b = int((blue / 255.0) * (2 ** 5 - 1) * brightness)
    r = int((red / 255.0) * (2 ** 5 - 1) * brightness)
    g = int((green / 255.0) * (2 ** 6 - 1) * brightness)

    # Shift the 5-bit blue and red to take the correct bit positions in the final color value
    bs = b << 8
    rs = r << 3

    # Shift the 6-bit green value, properly handling the 3 bits that overlflow to the beginning of the value
    g_high = g >> 3
    g_low = (g & 0b000111) << 13

    gs = g_high + g_low

    # Combine together the red, green, and blue values into a single color value
    color = bs + rs + gs

    return color


def read_bmp_to_buffer(lcd_display, file_handle):
    reader = bmpr.BMPFileReader(file_handle)

    for row_i in range(0, reader.get_height()):
        row = reader.get_row(row_i)
        for col_i, color in enumerate(row):
            lcd_display.pixel(
                col_i, row_i, to_color(color.red, color.green, color.blue)
            )


if __name__ == "__main__":
    
    # Setup the LCD display
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # max 65535

    lcd_display = lcd.LCD_1inch8()

    # Display a loading screen
    lcd_display.fill(lcd_display.BLACK)
    lcd_display.text("Loading...", 2, 28, lcd_display.WHITE)

    lcd_display.show()
    
    # Iterate through showing all of the BMP images in the images directory
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
            time.sleep(5)