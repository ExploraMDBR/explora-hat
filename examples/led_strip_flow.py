from explora.hat import ws281x as led_strip
from explora.hat import gpio_manager
from time import sleep
from math import sin, pi
from random import randint

#===========================
#======== CONTROLS =========
#===========================

NUM_LEDS = 20

MAX_V = 50 # Max Bright of leds

FLOW_SPEED = 5e-1
FLOW_W = 2 # Width: how many waves fit in the complete strip
TRANSITION_FACTOR = 1 # how much faster than the flow is the transition

REFRESH_HZ = 25

color_a = led_strip.Color(245,45,45)  # red
color_b = led_strip.Color(245,242,44) # yellow
color_c = led_strip.Color(44,167,245) # blue
off 	= led_strip.Color(0,0,0) 	  # black
colors = [color_a, color_b, color_c] 

for color in colors[:3]:
	color.v = MAX_V

print("Lighting initial CMY sequence")
for i in range(2):
	led_strip.set_leds(colors * int(NUM_LEDS / len(colors)))
	sleep(0.1)
	led_strip.set_leds([off] * NUM_LEDS)
	sleep(0.1)

print("Led Flow")


try:
	# prepare values for flow
	flow = 0
	transition_active = 0
	color_active = 0
	
	while 1:
		#----------- Transitions ------------
		if  flow /FLOW_SPEED % (REFRESH_HZ*2)  == 0: # once every two seconds
			transition_active = 0.001
			next_color = randint(0,len(colors)) % len(colors)
		
		c = colors[color_active]
		if transition_active == 0: 	# no transition
			leds = [c.copy() for _ in range(NUM_LEDS)] 

		else: 						# in transition
			nc = colors[next_color]
			
			leds = [c.copy() if i/NUM_LEDS > transition_active else nc.copy() for i in range(NUM_LEDS)]
			leds.reverse()

			# transition_active += FLOW_SPEED / TRANSITION_SLOWNESS
			transition_active += TRANSITION_FACTOR/REFRESH_HZ


			if transition_active > 1: # transition ended
				transition_active = 0
				color_active = next_color
				print("Transition ended, color active #{:d}: ".format( color_active ), colors[color_active])

		#----------- Flow ------------

		flow_strip = [sin((v/NUM_LEDS) * 2 * FLOW_W * pi + flow)  for v in range(NUM_LEDS)]

		for i, _c in enumerate(leds):
			leds[i].v = leds[i].v - (flow_strip[i] * 0.5 + 0.5) * MAX_V
			
		print("".join([led_strip.bright_to_ascii(c.v/MAX_V) for c in leds]), 
				"|", " ".join(["{:.2f}".format(c.v/MAX_V) for c in leds]),
				"| flow:", flow,
				"| trans: {:.2f}".format(transition_active))
		led_strip.set_leds(leds)
		flow += FLOW_SPEED
		
		sleep(1/REFRESH_HZ)

except KeyboardInterrupt:
	pass

the_color = led_strip.Color(0,0,0)
led_strip.set_leds([the_color]*NUM_LEDS)
led_strip.close()


	
