import time
import board
import digitalio
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const

# I2C Constants
I2C_ADDR = const(0x3C)
WIDTH = const(128)
HEIGHT = const(32)
BUFFER_SIZE = const(WIDTH * HEIGHT // 8)

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Command constants
_SET_CONTRAST = const(0x81)
_SET_DISPLAY_RAM = const(0xA4)
_SET_DISPLAY_ALL_ON = const(0xA5)
_SET_DISPLAY_NORMAL = const(0xA6)
_SET_DISPLAY_INVERTED = const(0xA7)
_SET_DISPLAY_OFF = const(0xAE)
_SET_DISPLAY_ON = const(0xAF)
_SET_START_LINE = const(0x40)
_SET_PAGE_ADDRESS = const(0xB0)

# Initialize OLED display
oled_device = I2CDevice(i2c, I2C_ADDR)

def write_command(cmd):
    with oled_device as i2c:
        i2c.write(bytearray([0x00, cmd]))

def write_data(data):
    with oled_device as i2c:
        i2c.write(bytearray([0x40] + data))

def init_display():
    write_command(_SET_DISPLAY_OFF)
    write_command(_SET_CONTRAST)
    write_command(0xCF)
    write_command(0xA1)  # Segment remap
    write_command(0xC8)  # COM Output scan direction
    write_command(0xA6)  # Normal display
    write_command(0xA8)  # Multiplex ratio
    write_command(0x1F)  # Duty = 1/32
    write_command(_SET_START_LINE)
    write_command(0x00)  # Set display offset
    write_command(0xA4)  # Set display to GDDRAM
    write_command(0xD3)  # Set display to GDDRAM
    write_command(0x00)  # Set display offset
    write_command(0xD5)  # Set display clock divide ratio/oscillator frequency
    write_command(0xF0)  # Set divide ratio
    write_command(0xD9)  # Set pre-charge period
    write_command(0x22)  # Set pre-charge period
    write_command(0xDA)  # Set COM pins hardware configuration
    write_command(0x12)
    write_command(0xDB)  # Set VCOMH
    write_command(0x20)  # Set VCOM deselect level
    write_command(0x8D)  # Set charge pump enable
    write_command(0x14)  # Enable charge pump
    write_command(_SET_DISPLAY_ON)

# Clear the display buffer
def clear_display():
    write_command(_SET_PAGE_ADDRESS)
    write_command(0)
    write_command(WIDTH // 8 - 1)
    for _ in range(HEIGHT // 8):
        write_command(0xB0)
        write_command(0x00)
        for _ in range(WIDTH):
            write_data(bytearray(1))

# Set a pixel in the display buffer
def set_pixel(x, y, color):
    if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
        if color:
            write_command(_SET_PAGE_ADDRESS)
            write_command(y // 8)
            write_command(WIDTH // 8 - 1)
            write_command(x)
            write_data(bytearray([1 << (y % 8)]))
        else:
            write_command(_SET_PAGE_ADDRESS)
            write_command(y // 8)
            write_command(WIDTH // 8 - 1)
            write_command(x)
            write_data(bytearray([0]))

# Update the display from the buffer
def update_display():
    with oled_device as i2c:
        i2c.write(bytearray([0x00, 0x22, 0x00, 0x07]))
    write_command(_SET_PAGE_ADDRESS)
    write_command(0)
    write_command(WIDTH // 8 - 1)
    for page in range(HEIGHT // 8):
        write_command(0xB0 | page)
        write_command(0)
        for col in range(WIDTH):
            write_data(display_buffer[col + page * WIDTH:col + page * WIDTH + 1])

# Initialize the display
init_display()
clear_display()

# Main loop
while True:
    # Your calculator logic goes here
    # You can use set_pixel() function to draw on the display buffer
    # Once the display buffer is updated, call update_display() to refresh the display
    time.sleep(0.1)
