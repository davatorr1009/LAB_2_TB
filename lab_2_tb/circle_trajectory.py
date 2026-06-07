#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CircleTrajectory(Node):
    def __init__(self):
        super().__init__('circle_trajectory')
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('angular_speed', 0.5)

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_cmd)
        self.get_logger().info('Trayectoria circular iniciada. Ctrl+C para detener.')

    def publish_cmd(self):
        msg = Twist()
        msg.linear.x = self.get_parameter('linear_speed').value
        msg.angular.z = self.get_parameter('angular_speed').value
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = CircleTrajectory()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
