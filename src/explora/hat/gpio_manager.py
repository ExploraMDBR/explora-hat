import threading

from os.path import join, realpath, dirname
import random
import sys, os, time
from sys import stdout
from gpiozero import Button, LED, Device
from gpiozero.exc import BadPinFactory

try:
	Device._default_pin_factory()
except BadPinFactory: #create dummy LED and Button classes
	from warnings import warn
	warn("Unable to load a suitable GPIO interface, no support for Buttons, LEDs or PMW")
	class Button:
		def __init__(self, _): pass
	class LED(Button):
		pass
# =====================================
# =           CONFIGURATION           =
# =====================================
DEBOUNCE = 0.1
# ======  End of CONFIGURATION  =======



#GPIO NUMBERS, no physical ones
buttons = [ Button(27), Button(9), Button(6),
		Button(19), Button(24), Button(20) ]
leds = [ LED(17), LED(10), LED(5),
		LED(13), LED(23), LED(16) ]

# ======  End of GLOBALS  =======

def dump_to_console(*args):
	args = [str(a) for a in args]
	print("[BTN MANAGER]", " ".join(args))
	stdout.flush()


class Button_Manager:
	def __init__(self, extra_btn = False):
		self.start_at = time.time()
		self.last_button = -1
		self.available = False

		self.button_press_handlers = []
		self.button_release_handlers = []
		self.last_btn_press = []
		self.is_btn_pressed = []

		global buttons
		global leds
		if extra_btn:
			buttons.append(Button(12))
			leds.append(LED(25))

		for i,btn in enumerate(buttons):
			self.button_press_handlers.append(self._default_handler)
			self.button_release_handlers.append(self._void_handler)

			self.last_btn_press.append(self.start_at)
			self.is_btn_pressed.append(False)
			
			btn.when_pressed = self.press_button
			btn.when_released = self.release_button  

		dump_to_console('Button manager started')

	def __del__(self):
		dump_to_console("Button manager ended")

	def press_button(self, button):
		number = buttons.index(button)

		global DEBOUNCE
		now = time.time()
		if now - self.last_btn_press[number] > DEBOUNCE:
			self.last_btn_press[number] = now
			self.is_btn_pressed[number] = True
			self.button_press_handlers[number](number, leds[number])

	def release_button(self, button):
		number = buttons.index(button)

		if self.is_btn_pressed[number]:
			self.is_btn_pressed[number] = False
			self.button_release_handlers[number](number, leds[number])


	def _default_handler(self, btn_n, led):
		print("Handler for button {} not set".format(btn_n))
	
	def _void_handler(self, btn_n, led):
		pass

	def set_press_handler(self, n, han):
		if n >= len(self.button_press_handlers):
			raise IndexError("Setting handler for button failed: Only {} buttons allowed".format(len(self.button_press_handlers)))

		self.button_press_handlers[n] = han

		dump_to_console('Added handler {} on button {}'.format(han.__name__, n ))

	def set_release_handler(self, n, han):
		if n >= len(self.button_release_handlers):
			raise IndexError("Setting handler for button failed: Only {} buttons allowed".format(len(self.button_release_handlers)))

		self.button_release_handlers[n] = han

		dump_to_console('Added handler {} on button {}'.format(han.__name__, n ))

