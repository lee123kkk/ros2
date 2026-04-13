import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # 거북이 제어용 메시지 타입

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        # /turtle1/cmd_vel 토픽으로 Twist 메시지를 발행하는 퍼블리셔 생성
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 0.1초마다 timer_callback 함수를 실행
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        # 직선 속도: 2.0 m/s (앞으로 이동)
        msg.linear.x = 2.0
        # 회전 속도: 1.8 rad/s (원형으로 회전)
        msg.angular.z = 1.8
        
        self.publisher_.publish(msg)
        self.get_logger().info('Sending velocity: linear=%0.1f, angular=%0.1f' 
                                % (msg.linear.x, msg.angular.z))

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()