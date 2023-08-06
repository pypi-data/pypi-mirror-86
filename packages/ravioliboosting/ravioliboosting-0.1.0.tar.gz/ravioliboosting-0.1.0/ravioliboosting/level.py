import keyboard
from pyautogui import *
import pyautogui
import time


def main():

	fight = False
	
	while keyboard.is_pressed("q") == False:


		if fight == False:
			print("walking")
			keyboard.send("a")
			time.sleep(0.1)
			keyboard.send("a")
			time.sleep(0.1)
			keyboard.send("d")
			time.sleep(0.1)
			keyboard.send("d")
			time.sleep(0.1)

			if pyautogui.pixel(100, 100) [0] == 0:
				print("LETS GET READY")
				time.sleep(4)
				fight = True


		if fight == True:
			print("fighting")
			keyboard.send("f")
			time.sleep(0.5)

			if pyautogui.pixel(100, 100) [0] == 0:
				print("EZ WE STOMPPED THEM")
				time.sleep(4)
				fight = False


main()