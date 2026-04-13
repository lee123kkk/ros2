import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')
        self.publisher_ = self.create_publisher(String, 'arduino_data', 10)
        
        # 주의: 2단계에서 확인한 포트 이름(/dev/ttyUSB0 또는 /dev/ttyACM0)으로 맞춰주세요!
        self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        
        self.timer = self.create_timer(0.05, self.read_serial)
        self.get_logger().info('Arduino Bridge Node가 시작되었습니다.')

    def read_serial(self):
        # 아두이노에서 넘어온 데이터가 있는지 확인
        if self.serial_port.in_waiting > 0:
            # 데이터를 읽고 쓸데없는 줄바꿈 기호를 잘라냅니다.
            line = self.serial_port.readline().decode('utf-8').rstrip()
            
            # 읽은 데이터를 ROS 2 String 토픽으로 발행합니다.
            msg = String()
            msg.data = line
            self.publisher_.publish(msg)
            self.get_logger().info(f'수신됨: {line}')

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()