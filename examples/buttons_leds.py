from explora.hat import gpio_manager
from time import sleep

counter = 0
button_pressed = False
btns = gpio_manager.Button_Manager(extra_btn = True) #use the PWM header as an extra button
leds = gpio_manager.leds

def light_led(num, the_led):
	global button_pressed
	for led in leds:
		led.off()

	the_led.on()
	button_pressed = True

def turn_off_led(num, the_led):
	the_led.off()

def light_all(num, the_led):
	for led in leds:
		led.on()

def turn_off_all(num, the_led):
	for led in leds:
		led.off()

for i in range(6):
	btns.set_press_handler(i, light_led)
	btns.set_release_handler(i, turn_off_led)

# The extra button lights all leds
btns.set_press_handler(6, light_all)
btns.set_release_handler(6, turn_off_all)

print("Looping leds, press a button or CTRL+C to control leds with buttons")
try:
	while 1:
		if button_pressed:
			break

		for led in leds:
			led.off()

		leds[counter%6].on()

		counter += 1
		sleep(0.2)

except KeyboardInterrupt:
	pass

finally:
	print("Press a button to light a led")


try:
	input("Press enter to end")
finally:
	print("exit")