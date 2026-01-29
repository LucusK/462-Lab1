import RPi.GPIO as GPIO
import time

#PIN NUMS
LED1_RED, LED1_GREEN, LED1_BLUE = 1, 2, 3
LED1 = [LED1_RED, LED1_GREEN, LED1_BLUE]

LED2_RED, LED2_GREEN, LED2_BLUE = 4, 5, 6
LED2 = [LED2_RED, LED2_GREEN, LED2_BLUE]

COUNT_SEG_A, COUNT_SEG_B, COUNT_SEG_C, COUNT_SEG_D, COUNT_SEG_E, COUNT_SEG_F, COUNT_SEG_G = 7, 8, 9, 10, 11, 12, 13
COUNT_SEGS = [COUNT_SEG_A, COUNT_SEG_B, COUNT_SEG_C, COUNT_SEG_D, COUNT_SEG_E, COUNT_SEG_F, COUNT_SEG_G]

BUTTON = 14

def set_LED1(red, green, blue):
    GPIO.output(LED1, (red, green, blue))

def set_LED2(red, green, blue):
    GPIO.output(LED2, (red, green, blue))


DIGIT_ORDER = [
    [1,1,1,1,1,1,0], #0
    [0,1,1,0,0,0,0], #1
    [1,1,0,1,1,0,1],#2
    [1,1,1,1,0,0,1],#3
    [0,1,1,0,0,1,1],#4
    [1,0,1,1,0,1,1],#5
    [1,0,1,1,1,1,1],#6
    [1,1,1,0,0,0,0],#7
    [1,1,1,1,1,1,1],#8
    [1,1,1,1,0,1,1]#9
]

def digit(num):
    order = DIGIT_ORDER[num]
    GPIO.output(COUNT_SEGS, order)



def main():
    GPIO.setmode(GPIO.BCM)

    OUTPUT_PINS = [LED1_RED, LED1_GREEN, LED1_BLUE, LED2_RED, LED2_GREEN, LED2_BLUE] + COUNT_SEGS
    GPIO.setup(OUTPUT_PINS, GPIO.OUT)
    #for pin in OUTPUT_PINS:
        #GPIO.setup(pin, GPIO.OUT)
    GPIO.output(OUTPUT_PINS, GPIO.LOW)

    GPIO.setup(BUTTON, GPIO.IN)

    #start
    set_LED2 = (0,1,0)
    set_LED1 = (1,0,0)

    GPIO.cleanup()


if __name__ == "__main__":
    main()