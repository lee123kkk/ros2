# 카메라를 켜서 영상을 읽고 /camera/image_raw라는 토픽으로 이미지를 쏘아 보내는 기본적인 퍼블리셔

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('webcam_pub')
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.033, self.timer_callback)
        
        # ▼ 여기서부터 수정된 부분입니다 ▼
        # 1. V4L2 드라이버를 명시적으로 사용합니다.
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2) 
        
        # 2. 영상 포맷을 가벼운 MJPEG로 강제 지정합니다. (WSL 병목 해결의 핵심!)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        # 3. 해상도를 640x480으로 낮춰서 가볍게 만듭니다.
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # ▲ 여기까지 ▲

        self.br = CvBridge()
        self.get_logger().info('Webcam Publisher Node가 시작되었습니다.')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            self.publisher_.publish(self.br.cv2_to_imgmsg(frame, encoding="bgr8"))
            self.get_logger().info('Publishing video frame')
        else:
            self.get_logger().warn('카메라 프레임을 읽어오지 못했습니다!')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = WebcamPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()