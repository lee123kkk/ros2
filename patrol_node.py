#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import time

def create_pose(navigator, x, y, z, w):
    """목표 지점의 좌표를 생성하는 함수"""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = 0.0
    pose.pose.orientation.w = w
    return pose

def main():
    rclpy.init()
    
    # 내비게이터 객체 생성 (RViz 역할을 대신함)
    navigator = BasicNavigator()

    # =========================================================
    # [실습과제 1] Rviz가 아닌 Node를 작성하여 로봇의 초기위치를 변경
    # =========================================================
    print("초기 위치를 설정합니다...")
    # 수정 후 (출력된 좌표 적용)
    initial_pose = create_pose(navigator, -1.958, -0.446, 0.0, 1.0)
    navigator.setInitialPose(initial_pose)

    # Nav2 서버가 활성화될 때까지 대기
    navigator.waitUntilNav2Active()
    print("내비게이션 시스템 준비 완료!")

    # 목표 지점 3곳 설정 (시작 지점 포함)
    goal_0 = initial_pose # 시작 지점
    goal_1 = create_pose(navigator, 1.5, 1.0, 0.0, 1.0) # 첫 번째 목표 (좌표는 맵에 맞게 수정 가능)
    goal_2 = create_pose(navigator, 1.5, -1.0, 0.0, 1.0) # 두 번째 목표

    # 순찰 경로 리스트
    patrol_route = [goal_0, goal_1, goal_2]
    
    # =========================================================
    # [실습과제 4] 무한히 순회하는 노드 (2, 3번 과제 동시 충족)
    # =========================================================
    print("무한 순찰 모드를 시작합니다. (종료: Ctrl+C)")
    
    while rclpy.ok():
        for i, goal in enumerate(patrol_route):
            print(f"목표 지점 {i}번으로 이동 중...")
            
            # [실습과제 2, 3] 목표 지점으로 이동하는 명령
            navigator.goToPose(goal)

            # 로봇이 목적지에 도착할 때까지 대기
            while not navigator.isTaskComplete():
                time.sleep(1.0) # 1초마다 상태 확인

            # 결과 확인
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                print(f"목표 지점 {i}번 도착 완료! 3초 대기 후 다음 지점으로 이동합니다.")
                time.sleep(3.0) # 도착 후 잠시 대기
            elif result == TaskResult.CANCELED:
                print("이동이 취소되었습니다.")
                break
            elif result == TaskResult.FAILED:
                print("이동에 실패했습니다. (장애물 등)")
                break

    # 종료 처리
    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
