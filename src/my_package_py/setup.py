from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_package_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.urdf'))), #(urdf 폴더 안의 모든 *.urdf 파일을 설치 폴더로 복사함)
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lee123kkk',
    maintainer_email='lee123kkk@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'talker = my_package_py.simple_publisher:main',
            'listener = my_package_py.simple_subscriber:main',
            'service_server = my_package_py.simple_service_server:main',
            'service_client = my_package_py.simple_service_client:main',
            'custom_talker = my_package_py.custom_publisher:main',
            'turtle_cmd = my_package_py.turtle_controller:main',
            'fibonacci_server = my_package_py.fibonacci_action_server:main',
            'fibonacci_client = my_package_py.fibonacci_action_client:main',
            'nav_server = my_package_py.nav_action_server:main',
            'nav_client = my_package_py.nav_action_client:main',
            'webcam_pub = my_package_py.webcam_pub:main',
            'arduino_bridge = my_package_py.arduino_bridge:main',
            'motor_server = my_package_py.motor_server:main',
            'motor_client = my_package_py.motor_client:main',
            'imu_pub = my_package_py.imu_publisher:main',
            'wifi_bridge = my_package_py.wifi_bridge:main',
            'teleop_node = my_package_py.teleop_node:main',
            'webcam_node = my_package_py.webcam_node:main',
        ],
    },
)
