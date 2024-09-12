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
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetLaunchConfiguration
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import xacro


def generate_launch_description():

    # Set the package name
    package_name = "origin_one_description"
    xacro_file_path = "urdf/origin_one.urdf.xacro"

    # Declare the drive_configuration argument
    arg_drive_configuration = DeclareLaunchArgument(
        "drive_configuration",
        default_value="skid_steer_drive",
        description="The drive configuration of the robot, either skid_steer_drive (which is default) or mecanum_drive.",
    )

    # Function to create the URDF description from the Xacro file
    def create_urdf_description(context):
        xacro_file = path.join(FindPackageShare(package_name).find(package_name), xacro_file_path)
        drive_configuration = LaunchConfiguration('drive_configuration').perform(context)
        urdf = xacro.process_file(xacro_file, mappings={"drive_configuration": drive_configuration}).toxml()
        return [SetLaunchConfiguration('urdf', urdf)]

    # Declare the namespace argument
    arg_ns = DeclareLaunchArgument(
        name="ns",
        default_value="robot",
        description="Namespace",
    )

    # Create the robot_state_publisher node
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace=LaunchConfiguration("ns"),
        parameters=[{"robot_description": ParameterValue(LaunchConfiguration('urdf'), value_type=str)}],
        respawn=False,
        respawn_delay=1.0,
        remappings=[("/joint_states", "/robot/joint_states")],
    )

    ld = LaunchDescription()
    ld.add_action(arg_drive_configuration)
    ld.add_action(OpaqueFunction(function=create_urdf_description))
    ld.add_action(arg_ns)
    ld.add_action(robot_state_publisher_node)


    return ld
