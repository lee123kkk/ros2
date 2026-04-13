import rclpy
from rclpy.node import Node
import serial
from my_msg_interface.srv import MotorCmd

class MotorServer(Node):
    def __init__(self):
        super().__init__('motor_server')
        # 서비스 서버 생성
        self.srv = self.create_service(MotorCmd, 'control_motor', self.motor_callback)
        
        # 아두이노 연결 (포트 이름이 다르면 수정하세요)
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            self.get_logger().info('모터 제어 서버 시작: 아두이노 연결 완료!')
        except serial.SerialException:
            self.get_logger().error('아두이노 연결 실패! 포트를 확인하세요.')

    def motor_callback(self, request, response):
        cmd = request.command
        
        if cmd == 'a' or cmd == 'b':
            # 아두이노로 문자 전송 (바이트 형태로 변환)
            self.serial_port.write(cmd.encode('utf-8'))
            response.success = True
            response.message = f"명령 '{cmd}' 실행 완료"
            self.get_logger().info(f"아두이노로 '{cmd}' 전송함")
        else:
            response.success = False
            response.message = "잘못된 명령 ('a' 또는 'b'만 입력하세요)"
            
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MotorServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()