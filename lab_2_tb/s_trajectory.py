#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class STrajectory(Node):
    def __init__(self):
        super().__init__('s_trajectory')
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('angular_speed', 0.5)
        self.declare_parameter('arc_duration', 3.0)  # segundos por arco

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_cmd)
        self.start_time = self.get_clock().now()
        self.get_logger().info('Trayectoria en S iniciada. Ctrl+C para detener.')

    def publish_cmd(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        arc_duration = self.get_parameter('arc_duration').value
        segment = int(elapsed / arc_duration)

        msg = Twist()
        msg.linear.x = self.get_parameter('linear_speed').value
        msg.angular.z = self.get_parameter('angular_speed').value * (1 if segment % 2 == 0 else -1)
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = STrajectory()
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
