import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class DummySlamTfNode(Node):
    def __init__(self):
        super().__init__('dummy_slam_tf')
        self.broadcaster = TransformBroadcaster(self)
        self.radius = 2.0
        self.angular_velocity = 0.5
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.publish_tf)

    def publish_tf(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds * 1e-9
        theta = self.angular_velocity * elapsed
        yaw = theta + math.pi / 2.0

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.radius * math.cos(theta)
        t.transform.translation.y = self.radius * math.sin(theta)
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(yaw / 2.0)
        t.transform.rotation.w = math.cos(yaw / 2.0)

        self.broadcaster.sendTransform(t)


def main():
    rclpy.init()
    rclpy.spin(DummySlamTfNode())
    rclpy.shutdown()
