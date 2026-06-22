import asyncio
import rclpy
from rclpy.node import Node
from bleak import BleakScanner
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from rclpy.time import Time
from ble_mapper_msgs.msg import BleDetection
from geometry_msgs.msg import Point


class BleNode(Node):
    def __init__(self):
        super().__init__('ble_mapper_ble')
        self.pub = self.create_publisher(BleDetection, 'ble_detections', 10)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.get_logger().info('Start')

    def get_current_position(self):
        try:
            tf = self.tf_buffer.lookup_transform('map', 'base_link', Time())
            p = tf.transform.translation
            return Point(x=p.x, y=p.y, z=p.z)
        except (
                LookupException, ConnectivityException, ExtrapolationException
        ) as e:
            self.get_logger().warn(f'TF取得失敗: {e}')
            return None

    def detection_callback(self, device, advertisement_data):
        pos = self.get_current_position()
        if pos is None:
            return

        msg = BleDetection()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.device_id = device.address
        msg.rssi = advertisement_data.rssi
        msg.position = pos
        self.pub.publish(msg)
        self.get_logger().info(
                f'検出: {device.address} RSSI={advertisement_data.rssi}')

    async def scan_loop(self):
        async with BleakScanner(self.detection_callback):
            while rclpy.ok():
                await asyncio.sleep(1.0)


def main():
    rclpy.init()
    node = BleNode()

    loop = asyncio.get_event_loop()
    ros_task = loop.run_in_executor(None, rclpy.spin, node)
    loop.run_until_complete(node.scan_loop())

    node.destroy_node()
    rclpy.shutdown()
