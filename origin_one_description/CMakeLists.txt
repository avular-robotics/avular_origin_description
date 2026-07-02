cmake_minimum_required(VERSION 3.8...3.22)
project(origin_one_description)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Testing
include(CTest)

# Install
ament_python_install_package(${PROJECT_NAME} SKIP_COMPILE)

include(GNUInstallDirs)
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY rviz DESTINATION share/${PROJECT_NAME})
install(DIRECTORY urdf/ DESTINATION share/${PROJECT_NAME}/urdf)
install(DIRECTORY urdf/meshes
        DESTINATION share/${PROJECT_NAME}/gz_resources/${PROJECT_NAME}/urdf)

# Create gazebo environment hooks
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/gz_resources.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/gz_resources.sh.in")

# Package
ament_package()
