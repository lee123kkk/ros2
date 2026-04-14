import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
import socket
import threading

class HybridWebcamNode(Node):
    def __init__(self):
        super().__init__('hybrid_webcam_node')
        self.client = self.create_client(SetBool, 'motor_control')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('모터 제어 서비스 대기 중...')

        # 윈도우에서 보내는 명령을 받을 UDP 서버 설정 (포트 9999)
        self.udp_ip = "0.0.0.0" 
        self.udp_port = 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))

        self.get_logger().info('우분투 수신 노드 시작! 윈도우의 비전 명령을 기다립니다.')

        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.receive_thread.start()

    def receive_loop(self):
        while rclpy.ok():
            try:
                # 윈도우 파이썬으로부터 데이터 수신
                data, _ = self.sock.recvfrom(1024)
                cmd = data.decode('utf-8')
                
                req = SetBool.Request()
                if cmd == "RUN":
                    req.data = True
                    self.get_logger().info('수신: RUN -> 모터 전진(F) 요청')
                elif cmd == "STOP":
                    req.data = False
                    self.get_logger().info('수신: STOP -> 모터 정지(S) 요청')
                else:
                    continue

                # wifi_bridge로 서비스 호출
                self.client.call_async(req)
            except Exception as e:
                self.get_logger().error(f"UDP 수신 에러: {e}")
                break

def main(args=None):
    rclpy.init(args=args)
    node = HybridWebcamNode()
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