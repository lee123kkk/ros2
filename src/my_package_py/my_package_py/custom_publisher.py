import rclpy
from rclpy.node import Node
# 우리가 만든 패키지에서 메시지 형식을 가져옵니다.
from my_msg_interface.msg import MyMsg 

class CustomPublisher(Node):
    def __init__(self):
        super().__init__('custom_publisher')
        # MyMsg 타입을 사용하도록 설정합니다.
        self.publisher_ = self.create_publisher(MyMsg, 'custom_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = MyMsg()
        msg.name = "Robot_Lee"
        msg.score = 100
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Name="%s", Score=%d' % (msg.name, msg.score))

def main(args=None):
    rclpy.init(args=args)
    node = CustomPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()