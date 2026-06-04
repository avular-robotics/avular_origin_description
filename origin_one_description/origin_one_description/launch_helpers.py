# Copyright 2026 Avular Holding B.V.
# All Rights Reserved
# You may use this code under the terms of the Avular
# Software End-User License Agreement.
#
# You should have received a copy of the Avular
# Software End-User License Agreement license with
# this file, or download it from: avular.com/eula
import os
from os import path
import tempfile, atexit, xacro

from launch import LaunchDescription
from launch.actions import OpaqueFunction, SetLaunchConfiguration
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


PACKAGE_NAME = "origin_one_description"
XACRO_FILE = "urdf/origin_one.urdf.xacro"
RVIZ_TEMPLATE = "rviz/origin_one.rviz"


def launch_robot_state_publisher(
    ld: LaunchDescription,
    drive_configuration=LaunchConfiguration("drive_configuration"),
    ns=LaunchConfiguration("ns"),
    tf_prefix=LaunchConfiguration("tf_prefix"),
    condition=None,
):
    """Add the URDF xacro processing + robot_state_publisher node to ``ld``.

    Remappings: joint_states -> /<ns>/joint_states; tf and tf_static -> global.
    Pass ``condition=IfCondition(...)`` to gate all added actions.
    """

    def _process_xacro(context):
        xacro_file = path.join(
            FindPackageShare(PACKAGE_NAME).find(PACKAGE_NAME), XACRO_FILE
        )
        urdf = xacro.process_file(
            xacro_file,
            mappings={
                "drive_configuration": (
                    drive_configuration.perform(context)
                    if hasattr(drive_configuration, "perform")
                    else str(drive_configuration)
                ),
                "prefix": (
                    tf_prefix.perform(context)
                    if hasattr(tf_prefix, "perform")
                    else str(tf_prefix)
                ),
            },
        ).toxml()
        return [SetLaunchConfiguration("urdf", urdf)]

    ld.add_action(OpaqueFunction(function=_process_xacro, condition=condition))
    ld.add_action(
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=["/", ns],
            parameters=[
                {
                    "robot_description": ParameterValue(
                        LaunchConfiguration("urdf"), value_type=str
                    )
                },
            ],
            respawn=False,
            respawn_delay=1.0,
            remappings=[
                ("joint_states", ["/", ns, "/joint_states"]),
                ("tf", "/tf"),
                ("tf_static", "/tf_static"),
            ],
            condition=condition,
        )
    )
    
def launch_rviz(
    ld: LaunchDescription,
    ns=LaunchConfiguration("ns"),
    tf_prefix=LaunchConfiguration("tf_prefix"),
    condition=None,
):
    """Render the .rviz template against ``ns``/``tf_prefix`` and launch rviz2.

    Pass ``condition=IfCondition(...)`` to gate the rviz2 node.
    """

    def _make_rviz_node(context):
        ns_value = ns.perform(context) if hasattr(ns, "perform") else str(ns)
        prefix_value = (
            tf_prefix.perform(context)
            if hasattr(tf_prefix, "perform")
            else str(tf_prefix)
        )
        p = f"{prefix_value}_" if prefix_value else ""

        template_path = os.path.join(
            FindPackageShare(PACKAGE_NAME).find(PACKAGE_NAME), RVIZ_TEMPLATE
        )
        with open(template_path, "r") as f:
            rendered = f.read()
        rendered = rendered.replace(
            "/robot/robot_description", f"/{ns_value}/robot_description"
        )
        rendered = rendered.replace(
            "Fixed Frame: base_link", f"Fixed Frame: {p}base_link"
        )

        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            prefix=f"{ns_value}_rviz_",
            suffix=".rviz",
            delete=False,
        )
        tmp.write(rendered)
        tmp.close()
        out_path = tmp.name

        atexit.register(
            lambda path=out_path: os.path.exists(path) and os.unlink(path)
        )

        return [
            Node(
                package="rviz2",
                executable="rviz2",
                name=f"rviz2_{ns_value}",
                arguments=["-d", out_path],
            )
        ]

    ld.add_action(OpaqueFunction(function=_make_rviz_node, condition=condition))
