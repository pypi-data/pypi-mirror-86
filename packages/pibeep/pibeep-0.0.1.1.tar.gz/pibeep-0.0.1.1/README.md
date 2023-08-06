# Summary

This is a beeping utility for the common buzzer. This package comes with a variety of beeps that can be called from a command line inteface or imported from python.

# Installation

To install simply install the pip package.

    pip install beep
	
You can then look at the examples on how to run as a cli. You can also import it into your project using,

	from beep import pulseBeep,beepDuration
	beepDuration(pin=12,duration=.33) #beeper on pin 12, on for .33 sec
	pulseBeep(pin=12,freq=25,duration=1) #pulse beep at 25HZ for 1 seccond


# Beeps

 - short: duration 0.05 sec
 - medium: duration 0.25 sec
 - long: duration 1.00 sec
 - warning: pulses 8HZ for 1.5 sec duration
 - confirmed: pulses 16HZ for .5 sec duration
 - brr: pulses 50HZ for .5 sec duration
 
# Example

The cli can be use any of the listed above beeps in the format as the following commands:

    beep.py warning --pin 12
	beep.py short --pin 12
	beep.py brr --pin 12

