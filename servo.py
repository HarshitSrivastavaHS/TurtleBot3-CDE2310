import RPi.GPIO as GPIO
import time


SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
	GPIO.output(SERVO_PIN, True)
	pwm.ChangeDutyCycle(angle/18+2)
	time.sleep(0.5)
	GPIO.output(SERVO_PIN, False)
	pwm.ChangeDutyCycle(0)
	time.sleep(0.5)

try:
	while True:
		print("Enter the angle: ")
		x = float(input())
		if x >= 0 and x <= 180:
			set_angle(x)
		else:
			print("Input an angle between 0 and 180")

except KeyboardInterrupt:
	print("End of program")
	pwm.stop()
	GPIO.cleanup() 
