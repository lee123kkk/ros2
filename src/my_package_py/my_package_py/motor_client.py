import sys
import rclpy
from rclpy.node import Node
from my_msg_interface.srv import MotorCmd

class MotorClient(Node):
    def __init__(self):
        super().__init__('motor_client')
        self.cli = self.create_client(MotorCmd, 'control_motor')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('서버 대기 중...')
        self.req = MotorCmd.Request()

    def send_request(self, cmd):
        self.req.command = cmd
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    
    # 터미널에서 'a' 또는 'b'를 입력받음
    if len(sys.argv) < 2:
        print("사용법: ros2 run my_package_py motor_client a (또는 b)")
        sys.exit(1)
        
    cmd_input = sys.argv[1]
    
    node = MotorClient()
    response = node.send_request(cmd_input)
    
    node.get_logger().info(f'서버 응답: {response.message}')
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()