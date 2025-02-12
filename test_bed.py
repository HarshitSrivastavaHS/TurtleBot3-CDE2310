#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np
import time
import RPi.GPIO as GPIO

# GPIO pin assignments (update as needed)
SERVO_PIN = 18
SOLENOID_PIN = 12

# Initialize the GPIO pins and PWM for the servo.
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)
    # Setup PWM on the servo pin at 50Hz
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)
    return pwm

# Function to set the servo to a given angle (in degrees)
def set_servo_angle(pwm, angle):
    # The duty cycle formula (angle/18 + 2) is based on your original code.
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(angle / 18.0 + 2)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)

# Function to trigger the solenoid plunger once.
def trigger_solenoid():
    GPIO.output(SOLENOID_PIN, GPIO.HIGH)
    # Hold the high state for a short period (adjust timing as needed)
    time.sleep(0.1)
    GPIO.output(SOLENOID_PIN, GPIO.LOW)
    time.sleep(0.1)

# ROS2 Node that subscribes to LaserScan and triggers the actions.
class TestBedNode(Node):
    def __init__(self, pwm):
        super().__init__('testbed_node')
        self.pwm = pwm
        # Create a subscription to the LaserScan topic (adjust topic name if needed)
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',   # topic from which LIDAR data is published
            self.scan_callback,
            10)
        # This flag is used so that the action is only triggered once per event.
        self.action_triggered = False

    def scan_callback(self, msg):
        # Convert the ranges list to a numpy array for easier processing.
        ranges = np.array(msg.ranges)
        # Replace zero values (if any) with NaN so they are ignored.
        ranges[ranges == 0] = np.nan
        # Get the minimum measured distance.
        min_distance = np.nanmin(ranges)
        self.get_logger().info(f"Min distance: {min_distance:.2f} m")
        # If the measured distance is less than or equal to 1m and we haven’t already triggered:
        if min_distance <= 1.0 and not self.action_triggered:
            self.get_logger().info("Distance threshold reached. Triggering servo and solenoid.")
            # Turn servo to 45 degrees
            set_servo_angle(self.pwm, 45)
            # Trigger the solenoid plunger
            trigger_solenoid()
            # Set flag so we don’t repeatedly trigger the action while the condition remains true.
            self.action_triggered = True
        # Reset the flag when the object is no longer too close.
        elif min_distance > 1.0:
            self.action_triggered = False

def main(args=None):
    rclpy.init(args=args)
    pwm = init_gpio()  # Initialize GPIO pins and PWM
    node = TestBedNode(pwm)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node due to KeyboardInterrupt")
    finally:
        # Clean up: destroy the node, shutdown ROS, stop PWM, and clean up GPIO.
        node.destroy_node()
        rclpy.shutdown()
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()

