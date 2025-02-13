import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
import os

class ObstacleTrigger(Node):
    def __init__(self):
        super().__init__('obstacle_trigger')

        # ✅ Match LIDAR QoS settings
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscribe to LIDAR scan topic
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            qos_profile
        )

        self.triggered = False  # ✅ Prevents repeated activation
        self.get_logger().info("Obstacle detection node started!")

    def lidar_callback(self, msg):
        num_ranges = len(msg.ranges)  # Total LIDAR points (typically 360)

        # ✅ Extract the last 5° (355°-360°) and first 5° (0°-5°)
        front_ranges = msg.ranges[-5:] + msg.ranges[:5]

        # ✅ Filter out invalid readings (e.g., 0.0 values)
        front_ranges = [r for r in front_ranges if r > 0.0]

        if front_ranges and min(front_ranges) < 0.5 and not self.triggered:
            self.get_logger().info("🚨 Obstacle detected in 10° front range! Running scripts...")

            # ✅ Run plunger and servo scripts
            os.system("python3 /home/ubuntu/turtlebot3_ws/plunger.py &")
            os.system("python3 /home/ubuntu/turtlebot3_ws/servo.py &")

            self.triggered = True  # ✅ Prevents continuous triggering

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleTrigger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
