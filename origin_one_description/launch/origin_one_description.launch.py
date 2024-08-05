# Copyright 2024 Avular B.V.
# All Rights Reserved
# You may use this code under the terms of the Avular
# Software End-User License Agreement.
#
# You should have received a copy of the Avular
# Software End-User License Agreement license with
# this file, or download it from: avular.com/eula

from os import path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    package_name = "origin_one_description"
    urdf_file_path = "urdf/origin_one.urdf"

    urdf = open(
        path.join(FindPackageShare(package_name).find(package_name), urdf_file_path)
    ).read()

    arg_ns = DeclareLaunchArgument(
        name="ns",
        default_value="",
        description="Namespace",
    )

    urdf_model_path_arg = DeclareLaunchArgument(
        name="urdf_model",
        default_value=PathJoinSubstitution(
            [FindPackageShare(package=package_name), urdf_file_path]
        ),
        description="Absolute path to robot urdf file.",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace=LaunchConfiguration("ns"),
        parameters=[{"robot_description": urdf}],
        respawn=False,
        respawn_delay=1.0,
        remappings=[("/joint_states", "/robot/joint_states")],
    )

    ld = LaunchDescription()
    ld.add_action(arg_ns)
    ld.add_action(urdf_model_path_arg)
    ld.add_action(robot_state_publisher_node)

    return ld
