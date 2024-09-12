## 1.1.0

- Moved to xacro for the URDF description.
- Added a drive_configuration = {skid_steer_drive, mecanum_drive} parameter to the description launch file.
- Changed both right wheel axes to have their z-axis pointing left, making positive rotation around the z-axis correspond to forward motion.
- Added mecanum wheel meshes and configuration to the URDF.
- Added MecanumDrive and OdometryPublisher gazebo plugin systems to the URDF.
- Changes the description topic from /description to /robot/robot_description.

## 1.0.0

- Changed the package name from origin_v10_description to origin_one_description and renamed all occurrences accordingly. 
- Removed the launch file robot_visualization_rviz.launch.py. 
- Added the launch file origin_one_description.launch.py which launches the robot state publisher.
- Added the launch file origin_one_rviz.launch.py for launching RVIZ. 
- Added link definitions for the IMU and ultrasonic sensors.

Contributors: @bobhendrikx4 @avupaul @tijsvdsmagt
