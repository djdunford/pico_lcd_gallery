import bmp_file_reader as bmpr
import uasyncio


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

    # Combine the red, green, and blue values into a single color value
    color = bs + rs + gs

    return color


async def read_bmp_to_buffer(lcd_display, file_handle):
    reader = bmpr.BMPFileReader(file_handle)

    offset = int((128 - reader.get_height()) / 2)
    print("Offset " + str(offset))

    for row_i in range(0, reader.get_height()):
        await uasyncio.sleep(0)
        row = reader.get_row(row_i)
        for col_i, color in enumerate(row):
            lcd_display.pixel(
                col_i, row_i + offset, to_color(color.red, color.green, color.blue)
            )
