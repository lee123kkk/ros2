#서버에게 숫자를 보내고 답을 기다리는 클라이언트

import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class SimpleServiceClient(Node):
    def __init__(self):
        super().__init__('simple_service_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        # 서버가 켜질 때까지 기다립니다.
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client = SimpleServiceClient()
    # 터미널에서 입력받은 인자값을 숫자로 변환하여 보냅니다.
    response = client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (int(sys.argv[1]), int(sys.argv[2]), response.sum))
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()