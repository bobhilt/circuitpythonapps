"""
    Visual acceleration mapper

    Based on acceleration level in each axis, map green for positive, red for negative.
    Brightness is higher for higher acceleration

"""

import time 
from adafruit_circuitplayground.express import cpx

#######################################
# Enable Debug Print

TEST = False

# Track max values
TRACK_MAX = True

max_accel = 0
max_brightness = 0
#######################################

red =   (255, 0, 0)
green = (0, 255, 0)
blue =  (0, 0, 255)

pixels = cpx.pixels
pixel_x = 7
pixel_y = 4
pixel_z = 0

def map_color(value):
    # if not much accel, blue.  Else green or red for + or - accel.
    if abs(value) < 3:
        color = blue
    elif value > 0:
        color = green
    else:
        color = red

    return color

def compute_brightness(values):
    # if there is high accel, make it brighter. low, dimmer
    avg_accel = sum([abs(x) for x in values])/3
    brightness = min(avg_accel, 25)/100
    
    if TEST: print("brightness: ", brightness)
    
    return brightness   #informational

def set_pixel(pixel, value):
    # modifies pixel colors
    pixels[pixel] = map_color(value)

def acceleration_lights(x, y, z):
    brightness = compute_brightness((x, y, z))

    # could affect individual brightness by changing color intesity
    # but brightness itself cannot be addressed to individual neopixels

    pixels.brightness = brightness 
    set_pixel(pixel_x, x)
    set_pixel(pixel_y, y)
    set_pixel(pixel_z, z)    
    
    if TRACK_MAX:
        global max_accel, max_brightness
        prev_max_accel = max_accel
        prev_max_brightness = max_brightness
        max_accel = max(max_accel, abs(x), abs(y), abs(z))
        max_brightness = max(max_brightness, brightness)
        if max_accel > prev_max_accel or max_brightness > prev_max_brightness:
            print('New max: Acceleration: {0} Brightness {1}'.format(max_accel, max_brightness))
            
while True:
    x,y,z = cpx.acceleration
    acceleration_lights(x,y,z)
    if TEST: 
        print((x,y,z))

    time.sleep(0.1)