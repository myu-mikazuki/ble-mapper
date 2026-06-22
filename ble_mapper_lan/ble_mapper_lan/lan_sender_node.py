import rclpy
from rclpy.node import Node
from ble_mapper_msgs.msg import BleDetection


class LanSenderNode(Node):
    def __init__(self):
        super().__init__('lan_sender')
        self.sub = self.create_subscription(
                BleDetection, '/ble_detections', self.send_cb, 10)

    def send_cb(self, msg):
        # requests.post(...) or socket.sendto(...)
        self.get_logger().info(f'デモ: メッセージが送信されました。({msg})')


def main():
    rclpy.init()
    rclpy.spin(LanSenderNode())
    rclpy.shutdown()
