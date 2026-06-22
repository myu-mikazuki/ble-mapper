import rclpy
from rclpy.node import Node
from ble_mapper_msgs.msg import BleDetection
from geometry_msgs.msg import Point
import random


class DummyBleNode(Node):
    def __init__(self):
        super().__init__('ble_detector')
        self.pub = self.create_publisher(BleDetection, 'ble_detections', 10)
        self.timer = self.create_timer(2.0, self.publish_dumy)

    def publish_dumy(self):
        msg = BleDetection()
        msg.device_id = 'AA:BB:CC:DD:EE:FF'
        msg.rssi = random.randint(-90, -40)
        msg.position = Point(x=1.0, y=2.0, z=0.0)
        msg.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(msg)
        self.get_logger().info(f'dummy 送信: RSSI={msg.rssi}')


def main():
    rclpy.init()
    rclpy.spin(DummyBleNode())
    rclpy.shutdown()
