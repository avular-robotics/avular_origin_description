# Copyright 2026 Avular Holding B.V.
# All Rights Reserved
# You may use this code under the terms of the Avular
# Software End-User License Agreement.
#
# You should have received a copy of the Avular
# Software End-User License Agreement license with
# this file, or download it from: avular.com/eula

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

from origin_one_description.launch_helpers import launch_robot_state_publisher
from origin_one_description.launch_helpers import launch_rviz


def generate_launch_description():
    ld = LaunchDescription()

    ld.add_action(
        DeclareLaunchArgument(
            "drive_configuration",
            default_value="skid_steer_drive",
            description=(
                "Drive configuration: skid_steer_drive (default), mecanum_drive, "
                "big_skid_steer_drive, or elevated_skid_steer_drive."
            ),
        )
    )
    ld.add_action(DeclareLaunchArgument("ns", default_value="robot"))
    ld.add_action(DeclareLaunchArgument("tf_prefix", default_value=""))
    ld.add_action(DeclareLaunchArgument("publish_robot_state", default_value="true"))

    launch_robot_state_publisher(
        ld, condition=IfCondition(LaunchConfiguration("publish_robot_state"))
    )
    launch_rviz(ld)

    return ld
