import rclpy
from rclpy.node import Node
import socket
from my_msg_interface.srv import MotorCmd

class WifiBridge(Node):
    def __init__(self):
        super().__init__('wifi_bridge')
        self.srv = self.create_service(MotorCmd, 'control_motor', self.motor_callback)
        
        # ESP32의 IP 주소와 포트 번호를 입력하세요 (시리얼 모니터에서 확인한 IP)
        self.esp32_ip = "192.168.0.61" 
        self.port = 8888
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.esp32_ip, self.port))
            self.get_logger().info('무선 연결(Wi-Fi) 성공! 모터 제어 준비 완료.')
        except Exception as e:
            self.get_logger().error(f'연결 실패! IP 주소나 ESP32 전원을 확인하세요: {e}')

    def motor_callback(self, request, response):
        try:
            # 클라이언트로부터 받은 'a' 또는 'b'를 Wi-Fi(소켓)를 통해 ESP32로 전송
            self.sock.send(request.command.encode('utf-8'))
            response.success = True
            response.message = f"명령 '{request.command}' 무선 전송 완료"
            self.get_logger().info(f"ESP32로 '{request.command}' 전송함")
        except Exception as e:
            response.success = False
            response.message = f"전송 오류: {str(e)}"
            self.get_logger().error(response.message)
            
        return response

def main(args=None):
    rclpy.init(args=args)
    node = WifiBridge() # 클래스 이름이 WifiBridge로 바뀜
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()