import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin assignments

BUTTON = 18

TL1_RED, TL1_GREEN, TL1_BLUE = 17, 27, 22
TL2_RED, TL2_GREEN, TL2_BLUE = 5, 6, 13

counts = {
    'a': 12,
    'b': 16,
    'c': 20,
    'd': 21,
    'e': 25,
    'f': 24,
    'g': 23
}

digits = {
    0: ['a','b','c','d','e','f'],
    1: ['b','c'],
    2: ['a','b','g','e','d'],
    3: ['a','b','c','d','g'],
    4: ['f','g','b','c'],
    5: ['a','f','g','c','d'],
    6: ['a','f','e','d','c','g'],
    7: ['a','b','c'],
    8: ['a','b','c','d','e','f','g'],
    9: ['a','b','c','d','f','g']
}

# gpio setup

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([TL1_RED, TL1_GREEN, TL1_BLUE, TL2_RED, TL2_GREEN, TL2_BLUE], GPIO.OUT)
GPIO.setup(list(counts.values()), GPIO.OUT)

# helpful functions

# controls for each RBG LED that supports both LEDs
def set_light(r, g, b, red, green, blue):
    GPIO.output(r, red)
    GPIO.output(g, green)
    GPIO.output(b, blue)

# displays the digit on the 7-segment display
def display_number(num):
    for seg in counts:
        GPIO.output(counts[seg], GPIO.LOW)
    for seg in digits[num]:
        GPIO.output(counts[seg], GPIO.HIGH)

# turns all segments of 7-segment display off, clears after countdown
def clear_display():
    for seg in counts:
        GPIO.output(counts[seg], GPIO.LOW)

# traffic light logic
def pedestrian_sequence():
    # light 2 blinks blue 3 times
    for _ in range(3):
        set_light(TL2_RED, TL2_GREEN, TL2_BLUE, 0, 0, 1)
        time.sleep(0.5)
        set_light(TL2_RED, TL2_GREEN, TL2_BLUE, 0, 0, 0)
        time.sleep(0.5)

    # pedestrians can go and cars stoop
    set_light(TL2_RED, TL2_GREEN, TL2_BLUE, 1, 0, 0)
    set_light(TL1_RED, TL1_GREEN, TL1_BLUE, 0, 1, 0)

    # countdown from 9
    for count in range(9, -1, -1):
        display_number(count)

        # starts blinking blue when we hit 4 seconds
        if count <= 4:
            set_light(TL1_RED, TL1_GREEN, TL1_BLUE, 0, 0, 1)

        time.sleep(1)
    
    clear_display()

    # reset the lights
    set_light(TL1_RED, TL1_GREEN, TL1_BLUE, 1, 0, 0)
    set_light(TL2_RED, TL2_GREEN, TL2_BLUE, 0, 1, 0)

# polling logic

COOLDOWN = 20
last_press = 0
'''
# Default state
set_light(TL1_RED, TL1_GREEN, TL1_BLUE, 1, 0, 0)
set_light(TL2_RED, TL2_GREEN, TL2_BLUE, 0, 1, 0)

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:
            current_time = time.time()
            if current_time - last_press >= COOLDOWN:
                last_press = current_time
                pedestrian_sequence()

        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
'''

def main():
    GPIO.setmode(GPIO.BCM)

    OUTPUT_PINS = [TL1_RED, TL1_GREEN, TL1_BLUE, TL2_RED, TL2_GREEN, TL2_BLUE] + COUNT_SEGS
    GPIO.setup(OUTPUT_PINS, GPIO.OUT)
    #for pin in OUTPUT_PINS:
        #GPIO.setup(pin, GPIO.OUT)
    GPIO.output(OUTPUT_PINS, GPIO.LOW)

    GPIO.setup(BUTTON, GPIO.IN)

    #start
    set_LED2 = (0,1,0)
    set_LED1 = (1,0,0)

    try:
        while True:
            set_LED2 = (0,1,0)
            set_LED1 = (1,0,0)
            poll()
            run()
            time.sleep(1) #prevent spamming
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
