import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('pick_place_demo')
    world_path = os.path.join(pkg_share, 'worlds', 'pick_place.sdf')

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    # Bridge Gazebo <-> ROS2 topics (clock is essential)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    # Spawns panda_arm from robot_description topic
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'panda', '-topic', 'robot_description'],
        output='screen'
    )

    return LaunchDescription([gz_sim, bridge, spawn])
