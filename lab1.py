import RPi.GPIO as GPIO
import time

#PIN NUMS
LED1_RED, LED1_GREEN, LED1_BLUE = 1, 2, 3
LED2_RED, LED2_GREEN, LED2_BLUE = 4, 5, 6

COUNT_SEG_A, COUNT_SEG_B, COUNT_SEG_C, COUNT_SEG_D, COUNT_SEG_E, COUNT_SEG_F = 7, 8, 9, 10, 11, 12

BUTTON = 13


def main():
    GPIO.setmode(GPIO.BCM)

if __name__ == "__main__":
    main()