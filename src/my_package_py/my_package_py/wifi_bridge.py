import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool  # 서비스 타입 추가
import socket
import threading

class WifiBridgeNode(Node):
    def __init__(self):
        super().__init__('wifi_bridge_node')
        self.imu_pub = self.create_publisher(String, 'imu_data', 10)
        
        # 1. 모터 제어용 서비스 서버 생성 (웹캠 노드가 호출할 서비스)
        self.srv = self.create_service(SetBool, 'motor_control', self.motor_control_callback)

        self.esp32_ip = '192.168.0.61'
        self.esp32_port = 8888
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.sock.connect((self.esp32_ip, self.esp32_port))
            self.get_logger().info('ESP32 연결 성공! 서비스 서버 대기 중...')
        except Exception as e:
            self.get_logger().error(f'연결 실패: {e}')
            return

        # 아두이노에 데이터 요청('R')을 보내는 타이머
        self.timer = self.create_timer(0.5, self.request_data)
        self.receive_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.receive_thread.start()

    # 2. 서비스 요청이 들어왔을 때 실행되는 콜백 함수
    def motor_control_callback(self, request, response):
        # request.data가 True면 'F'(전진), False면 'S'(정지)
        cmd = 'F' if request.data else 'S'
        try:
            self.sock.sendall(cmd.encode('utf-8'))
            self.get_logger().info(f'웹캠 서비스 요청 받음 -> ESP32 전송: {cmd}')
            response.success = True
            response.message = f"Motor set to {cmd}"
        except Exception as e:
            response.success = False
            response.message = str(e)
            self.get_logger().error(f'전송 에러: {e}')
        
        return response

    def request_data(self):
        try:
            self.sock.sendall(b'R')
        except:
            pass

    def receive_data(self):
        buffer = ""
        while rclpy.ok():
            try:
                data = self.sock.recv(1024).decode('utf-8', errors='ignore')
                if not data: break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if 'IMU' in line:
                        clean_line = line[line.find('IMU'):]
                        imu_msg = String()
                        imu_msg.data = clean_line
                        self.imu_pub.publish(imu_msg)
            except:
                break

def main(args=None):
    rclpy.init(args=args)
    node = WifiBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()