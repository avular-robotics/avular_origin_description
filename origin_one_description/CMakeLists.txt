cmake_minimum_required(VERSION 3.16)

project(origin_one_description)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Testing
include(CTest)

# Install
ament_python_install_package(${PROJECT_NAME} SKIP_COMPILE)

include(GNUInstallDirs)
install(DIRECTORY launch DESTINATION ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME})
install(DIRECTORY rviz DESTINATION ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME})
install(DIRECTORY urdf DESTINATION ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME})

# Package
ament_package()
