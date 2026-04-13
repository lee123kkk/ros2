import time
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from my_msg_interface.action import MoveToTarget

class NavActionServer(Node):
    def __init__(self):
        super().__init__('nav_action_server')
        
        # 1. 다차선 동시 처리를 위한 콜백 그룹
        self.cb_group = ReentrantCallbackGroup()
        
        # 2. 액션 서버 생성 (취소 콜백 연결 포함)
        self._action_server = ActionServer(
            self,
            MoveToTarget,
            'move_to_target',
            self.execute_callback,
            callback_group=self.cb_group,
            cancel_callback=self.cancel_callback
        )
        
        self.current_x = 0.0
        self.current_y = 0.0
        self.get_logger().info('Navigation Action Server is ready.')

    # 3. 취소 요청을 무조건 수락(ACCEPT)하는 함수
    def cancel_callback(self, cancel_request):
        self.get_logger().warn('클라이언트의 취소 요청을 수락합니다!')
        return CancelResponse.ACCEPT

    # 4. 실제 주행을 수행하는 함수
    def execute_callback(self, goal_handle):
        target_x = goal_handle.request.target_x
        target_y = goal_handle.request.target_y
        self.get_logger().info(f'목표 수신: 이동 좌표 ({target_x}, {target_y})')

        feedback_msg = MoveToTarget.Feedback()

        while True:
            # 주행 중 취소 요청이 수락되었는지 확인
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = MoveToTarget.Result()
                result.success = False
                result.message = "클라이언트 요청으로 주행이 취소되었습니다."
                self.get_logger().info('목표가 취소되었습니다.')
                return result

            dist = math.sqrt((target_x - self.current_x)**2 + (target_y - self.current_y)**2)
            
            if dist < 0.5:
                break

            self.current_x += (target_x - self.current_x) * 0.2
            self.current_y += (target_y - self.current_y) * 0.2

            feedback_msg.distance_remaining = dist
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'피드백: 남은 거리 {dist:.2f}')
            
            time.sleep(1.0)

        goal_handle.succeed()
        result = MoveToTarget.Result()
        result.success = True
        result.message = "목표 지점에 성공적으로 도착했습니다!"
        self.get_logger().info('목표 달성 성공.')
        return result

def main(args=None):
    rclpy.init(args=args)
    node = NavActionServer()
    # 멀티 스레드 실행기 적용
    executor = MultiThreadedExecutor()
    try:
        rclpy.spin(node, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()