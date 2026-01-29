import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)   # ignore channel-in-use warnings
GPIO.setmode(GPIO.BCM)  

LED1_RED, LED1_GREEN, LED1_BLUE = 17, 27, 22
LED1 = [LED1_RED, LED1_GREEN, LED1_BLUE]

LED2_RED, LED2_GREEN, LED2_BLUE = 5, 6, 13
LED2 = [LED2_RED, LED2_GREEN, LED2_BLUE]

COUNT_SEG_A, COUNT_SEG_B, COUNT_SEG_C, COUNT_SEG_D, COUNT_SEG_E, COUNT_SEG_F, COUNT_SEG_G = 12, 16, 20, 21, 25, 24, 26
COUNT_SEGS = [COUNT_SEG_A, COUNT_SEG_B, COUNT_SEG_C, COUNT_SEG_D, COUNT_SEG_E, COUNT_SEG_F, COUNT_SEG_G]

BUTTON = 18

DIGIT_ORDER = [
    [1,0,1,1,1,1,1], #0
    [1,0,0,0,1,0,0], #1
    [0,1,0,1,1,1,1], #2
    [1,1,0,1,1,1,0], #3
    [1,1,1,0,1,0,0], #4
    [1,1,1,1,0,1,0], #5
    [1,1,1,1,0,1,1], #6
    [1,0,0,1,1,0,0], #7
    [1,1,1,1,1,1,1], #8
    [1,1,1,1,1,1,0]  #9
]

SEG_NAMES = ["A","B","C","D","E","F","G"]


# LEDs
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

# 7-segment
GPIO.setup(COUNT_SEGS, GPIO.OUT)

# Button with internal pull-up
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def set_LED1(red, green, blue):
    GPIO.output(LED1, (red, green, blue))

def set_LED2(red, green, blue):
    GPIO.output(LED2, (red, green, blue))

def digit(num):
    order = DIGIT_ORDER[num]
    GPIO.output(COUNT_SEGS, order)

def segment_test(on_level=1):
    GPIO.output(COUNT_SEGS, 0 if on_level == 1 else 1)  # all off
    for idx, pin in enumerate(COUNT_SEGS):
        GPIO.output(COUNT_SEGS, 0 if on_level == 1 else 1)  # all off
        GPIO.output(pin, on_level)  # turn one on
        print("This should be segment", SEG_NAMES[idx], "on pin", pin)
        time.sleep(1)
    GPIO.output(COUNT_SEGS, 0 if on_level == 1 else 1)


def run():
    # LED2 becomes blue, blink 3 times, then red
    for _ in range(3):
        set_LED2(0, 0, 1)
        time.sleep(0.5)
        set_LED2(0, 0, 0)
        time.sleep(0.5)
    set_LED2(1, 0, 0)

    # After red, LED1 green, countdown
    for i in range(9, -1, -1):
        digit(i)
        if i >= 5:
            set_LED1(0, 1, 0)  # green
            time.sleep(2)
        else:
            # blink blue
            for _ in range(2):
                set_LED1(0, 0, 1)
                time.sleep(0.5)
                set_LED1(0, 0, 0)
                time.sleep(0.5)

    # done
    set_LED1(1, 0, 0)
    set_LED2(0, 1, 0)


def button_pressed_callback(channel):
    print("Button pressed! Starting run sequence...")
    run()


def main():

    # Add falling edge detection with debounce
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)

    print("System ready. Press the button to run the sequence.")

    try:
        while True:
            time.sleep(0.1)  # keep program alive
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()

