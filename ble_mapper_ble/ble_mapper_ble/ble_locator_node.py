import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from ble_mapper_msgs.msg import BleDetection
from ble_mapper_msgs.msg import BleObservation
from geometry_msgs.msg import Pose


class BleLocatorNode(Node):
    def __init__(self):
        super().__init__('ble_locator')

        self.pub = self.create_publisher(
                BleObservation, 'ble_observations', 10)

        self.sub = self.create_subscription(
                BleDetection, 'ble_detections', self.detection_callback, 10)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.get_logger().info('Start')

    def get_current_pose(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                    'map', 'base_link', Time())
            position = tf.transform.translation

            pose = Pose()
            pose.position.x = position.x
            pose.position.y = position.y
            pose.position.z = position.z
            pose.orientation = tf.transform.rotation

            return pose
        except (
                LookupException, ConnectivityException, ExtrapolationException
        ) as e:
            self.get_logger().warn(f'TF取得失敗: {e}')
            return None

    def detection_callback(self, detection: BleDetection):
        pose = self.get_current_pose()
        if pose is None:
            return

        msg = BleObservation()
        msg.detection = detection
        msg.pose = pose
        self.pub.publish(msg)
        self.get_logger().info(
                f'検出: {detection.device_id} RSSI={detection.rssi}')


def main():
    rclpy.init()
    rclpy.spin(BleLocatorNode())
    rclpy.shutdown()
