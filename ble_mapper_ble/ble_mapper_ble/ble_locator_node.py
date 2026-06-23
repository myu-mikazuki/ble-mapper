import asyncio
import rclpy
from rclpy.node import Node
from bleak import BleakScanner
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from rclpy.time import Time
from ble_mapper_msgs.msg import BleDetection
from geometry_msgs.msg import Point

class BleLocatorNode(Node):
    def __init__(self):
        super().__init__('ble_locator')

        self.pub = self.create_publisher(BleObservation, 'ble_observations', 10)

        self.sub = self.create_subscription(BleDetection, 'ble_detections', self.detection_callback, 10)

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

    def detection_callback(self, detection: BleDetection):
        pos = self.get_current_position()
        if pos is None:
            return

        msg = BleObservation()
        msg.detection = detection
        msg.position = pos
        self.pub.publish(msg)
        self.get_logger().info(
                f'検出: {device.address} RSSI={advertisement_data.rssi}')
