import RPi.GPIO as GPIO

# Define GPIO pin
SOLENOID_PIN = 12  # Change this if using a different pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(SOLENOID_PIN, GPIO.OUT)  # Set pin as output

def activate_solenoid():
    GPIO.output(SOLENOID_PIN, GPIO.HIGH)  # Turn solenoid ON
    print("Solenoid Activated")

def deactivate_solenoid():
    GPIO.output(SOLENOID_PIN, GPIO.LOW)  # Turn solenoid OFF
    print("Solenoid Deactivated")

try:
    while True:
        cmd = input("Enter 'on' to activate, 'off' to deactivate, 'exit' to quit: ").strip().lower()
        if cmd == "on":
            activate_solenoid()
        elif cmd == "off":
            deactivate_solenoid()
        elif cmd == "exit":
            break
        else:
            print("Invalid command. Use 'on', 'off', or 'exit'.")
except KeyboardInterrupt:
    print("\nProgram interrupted.")

finally:
    GPIO.cleanup()  # Reset GPIO settings
    print("GPIO cleaned up.")

