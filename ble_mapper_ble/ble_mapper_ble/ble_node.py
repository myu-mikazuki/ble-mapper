import asyncio
from threading import Thread
import rclpy
from rclpy.node import Node
from bleak import BleakScanner
from ble_mapper_msgs.msg import BleDetection


class BleNode(Node):
    def __init__(self):
        super().__init__('ble_mapper_ble')
        self.pub = self.create_publisher(BleDetection, 'ble_detections', 10)
        self.get_logger().info('Start')

    def detection_callback(self, device, advertisement_data):
        msg = BleDetection()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.device_id = device.address
        msg.rssi = advertisement_data.rssi
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

    executor_thread = Thread(target=rclpy.spin, args=(node, ), daemon=True)
    executor_thread.start()
    asyncio.run(node.scan_loop())

    node.destroy_node()
    rclpy.shutdown()
