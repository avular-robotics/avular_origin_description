# Avular Origin Model for Gazebo Simulation

This model contains the Avular Origin model for simulation. This is a simplified model designed to get started immediatly.

It has the following sensors included in the model:
* Ouster OS1-32
* Realsense D435
* GNSS

It is controlled through a diff-drive plugin which mimics the skidsteer that the actual origin also has.

A `ros_gz_bridge` configuration has been supplied to easily start using it with ROS.

The Origin as supplied by Avular will have some additional features and interaction requirements. 
For more information about this, see our [examples repository](https://github.com/avular-robotics/example_origin_ros).

## Getting Started

Simply use the official tutorial found [here](https://gazebosim.org/docs/harmonic/fuel_insert)

Or you can do one of the following:

### Fuel

You can simply include it as:

```xml
<include>
  <uri>
    https://fuel.gazebosim.org/1.0/AvularRobotics/models/AvularOriginOne
  </uri>
</include>
```

This you can do in your world directly, or use it as a basis for your own robot:

Or build your own robot with this robot as a base. E.g. if you want to add a new sensor to it:

```xml
<model name="modified_origin">
    <include>
    <uri>
        https://fuel.gazebosim.org/1.0/AvularRobotics/models/AvularOriginOne
    </uri>
    </include>

    <!-- Custom sensor -->
    <plugin filename="your-sensor-system" name="Your::Sensor::System">
    </plugin>
    <link name="your_new_sensor_link">
      <!-- At [0.2, 0.0, 0.3] from base_link -->
      <pose>0.2 0.0 0.3 0 0 0</pose>
      <!-- Add visuals/collision -->
      <!-- Modify to the sensor you want -->
      <sensor name="your_sensor" type="your_sensor">
        <!-- Fill -->
      </sensor>
    </link>
</model>
```

### Download and spawn
Alternative to download this model and use it locally. If you have a simulation server running, you can spawn it as:

```bash
ros2 run ros_gz_sim create -name Origin -file /path/to/origin/model.sdf 
```

## Ros Bridge

To use the ros_gz_bridge to allow communication with the robot through ROS, run the following node:
```bash
ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=/path/to/origin/ros_bridge.yaml
```

## GNSS
The GNSS plugin will only work if you have spherical coordinates defined for your world. This will look something like:
```xml
<!-- Spherical coordinates for navsat plugin -->
<spherical_coordinates>
    <surface_model>EARTH_WGS84</surface_model>
    <world_frame_orientation>ENU</world_frame_orientation>
    <latitude_deg>51.573157</latitude_deg>
    <longitude_deg>5.657958</longitude_deg>
    <elevation>0</elevation>
    <heading_deg>0</heading_deg>
</spherical_coordinates>
```

If you try to subscribe to the GNSS topic without having these spherical coordinates, it will start giving errors in the gazebo server. This is due to the implementation of the default NavSat plugin.
