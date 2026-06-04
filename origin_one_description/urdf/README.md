# Avular Origin One URDF

This directory contains the URDF/xacro description for the Avular Origin One,
along with the mesh files it references.

```
urdf/
├── origin_one.urdf.xacro   # Robot description
└── meshes/                 # body, wheel, ouster, antenna meshes
```

The xacro is the single source of truth for the robot's kinematic and visual
description. It is consumed by `robot_state_publisher` (via the package's
launch files) and implicitly converted to SDF by Gazebo at spawn time via the
`avular_simulations` / `gazebo_simulation` packages


## Model overview

| Link                  | Type       | Notes                                                            |
|-----------------------|------------|------------------------------------------------------------------|
| `base_link`           | root       | Empty frame; ground-level origin at the center of the robot footprint |
| `main_body`           | fixed      | Body collision box (0.65 × 0.4 × 0.125), `body.obj` visual; raised `groundClearance` above `base_link` |
| `left_front_wheel`    | continuous | Wheel mesh varies with `drive_configuration`                     |
| `right_front_wheel`   | continuous | Wheel mesh varies with `drive_configuration`                     |
| `left_rear_wheel`     | continuous | Wheel mesh varies with `drive_configuration`                     |
| `right_rear_wheel`    | continuous | Wheel mesh varies with `drive_configuration`                     |
| `ouster_base`         | fixed      | Ouster base mount, `ouster.obj` visual                               |
| `os_sensor`           | fixed      | Ouster sensor housing frame                                      |
| `camera_link`         | fixed      | RealSense D435 mount                                             |
| `gnss_link`           | fixed      | GNSS antenna, `antenna.obj` visual                               |
| `imu_link`            | fixed      | IMU mounting frame                                               |
| `us_{lf,cf,rf,lr,cr,rr}_link` | fixed | Six ultrasonic sensor frames (left/center/right × front/rear) |

`base_link → main_body` is offset vertically by `groundClearance`, which
varies with the drive configuration. All other sensor and wheel joints are
attached to `main_body`.

The wheel joints are `continuous` with a velocity limit of 10. Driving them in RViz requires a
`/<ns>/joint_states` topic (the launch file defaults `<ns>` to `robot`, so
`/robot/joint_states`).

## Drive configurations

The `drive_configuration` xacro arg selects the wheel geometry and ground
clearance. Track width and wheelbase are picked to match the physical robot
in each configuration:

| Configuration             | Track  | Wheelbase | Wheel radius | Ground clearance | Wheel mesh         |
|---------------------------|--------|-----------|--------------|------------------|--------------------|
| `skid_steer_drive`        | 0.500  | 0.410     | 0.1200       | 0.0640           | `wheel.obj`        |
| `big_skid_steer_drive`    | 0.530  | 0.410     | 0.1650       | 0.1090           | `wheel_big.obj`    |
| `mecanum_drive`           | 0.475  | 0.410     | 0.1015       | 0.0455           | `wheel_mecanumA.obj` / `wheel_mecanumB.obj` |

All values are in metres.

> Note: an `elevated_skid` configuration exists in the code, but it currently behaves the same as `big_skid_steer_drive` and is not yet supported.

## Xacro arguments

| Arg                   | Default            | Description                                                     |
|-----------------------|--------------------|-----------------------------------------------------------------|
| `drive_configuration` | `skid_steer_drive` | One of `skid_steer_drive`, `big_skid_steer_drive`, `mecanum_drive`. Picks wheel mesh and the kinematic parameters in the table above. |
| `prefix`              | `""`               | Optional link/joint prefix. When non-empty, every link/joint name is prefixed with `<prefix>_`. Use this to spawn multiple Origin Ones in the same world without TF name collisions. |

## Rendering the xacro manually

```bash
# Plain render (default skid_steer_drive)
xacro origin_one.urdf.xacro > origin_one.urdf

# Mecanum configuration
xacro origin_one.urdf.xacro drive_configuration:=mecanum_drive > origin_one_mecanum.urdf

# Big skid steer drive configuration
xacro origin_one.urdf.xacro drive_configuration:=big_skid_steer_drive > origin_one_big_wheels.urdf

# With a prefix (e.g. for multi-robot setups)
xacro origin_one.urdf.xacro prefix:=origin > origin_one_prefixed.urdf
```

In normal use you don't need to do this — the launch files in
[../launch/] process the xacro for you and pass it to
`robot_state_publisher` via the `robot_description` parameter.

## Meshes

Meshes are referenced as
`package://origin_one_description/urdf/meshes/<file>.obj` with a uniform
`0.001 0.001 0.001` scale (the meshes are authored in millimetres). They are
Wavefront `.obj` files with sibling `.mtl` material files. The mecanum
configuration uses two different wheel meshes (`wheel_mecanumA.obj` and
`wheel_mecanumB.obj`) for the left and right rollers; all other
configurations use the same mesh on every wheel and rely on per-wheel visual
RPY to flip orientation.
