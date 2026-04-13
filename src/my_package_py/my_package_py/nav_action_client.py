import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_msg_interface.action import MoveToTarget
from action_msgs.msg import GoalStatus

class NavActionClient(Node):
    def __init__(self):
        super().__init__('nav_action_client')
        self._action_client = ActionClient(self, MoveToTarget, 'move_to_target')
        self._goal_handle = None
        self._cancel_future = None  # 취소 증거 보관용

    def send_goal(self, x, y):
        self.get_logger().info('서버 대기 중...')
        self._action_client.wait_for_server()

        goal_msg = MoveToTarget.Goal()
        goal_msg.target_x = float(x)
        goal_msg.target_y = float(y)

        self.get_logger().info(f'목표 전송: ({x}, {y})')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self._goal_handle = future.result()
        if not self._goal_handle.accepted:
            self.get_logger().info('목표가 서버에 의해 거절되었습니다.')
            return
        
        self.get_logger().info('목표가 수락되었습니다. 주행 시작!')
        self._get_result_future = self._goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        dist = feedback_msg.feedback.distance_remaining
        self.get_logger().info(f'수신된 피드백 - 남은 거리: {dist:.2f}')

        # 아직 취소 안 했을 때만 취소 요청!
        if dist > 20.0 and self._cancel_future is None:
            self.get_logger().warn('거리가 너무 멉니다! 주행 취소를 요청합니다.')
            self._cancel_future = self._goal_handle.cancel_goal_async()

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        
        if status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn(f'결과: 확실하게 취소됨! - {result.message}')
        elif status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f'결과: 성공 - {result.message}')
        else:
            self.get_logger().info(f'결과: 기타 상태 (코드: {status})')
            
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    client = NavActionClient()
    client.send_goal(30.0, 40.0) 
    try:
        rclpy.spin(client)
    except KeyboardInterrupt:
        pass
    finally:
        client.destroy_node()

if __name__ == '__main__':
    main()