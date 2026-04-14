import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys, select, termios, tty

msg = """
---------------------------
F : 전진 (Forward)
S : 정지 (Stop)
CTRL-C : 종료
---------------------------
"""

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = rclpy.create_node('teleop_node')
    pub = node.create_publisher(String, 'motor_cmd', 10)

    try:
        print(msg)
        while True:
            key = get_key(settings)
            if key.lower() == 'f':
                pub.publish(String(data='F'))
                print("\r명령: 전진 (F)   ", end="")
            elif key.lower() == 's':
                pub.publish(String(data='S'))
                print("\r명령: 정지 (S)   ", end="")
            elif key == '\x03': # CTRL-C
                break
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()