from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package_py',
            executable='wifi_bridge',
            name='wifi_bridge_node',
            output='screen'
        )
    ])