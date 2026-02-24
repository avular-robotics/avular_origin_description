cmake_minimum_required(VERSION 3.16)

find_package(cmake_avular REQUIRED)
parse_manifest("${CMAKE_CURRENT_SOURCE_DIR}/package.xml")
project(
  ${PROJECT_NAME}
  VERSION ${PROJECT_VERSION}
  DESCRIPTION ${PROJECT_DESCRIPTION})

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Testing
include(CTest)
add_copyright_test()

# Install
ament_python_install_package(${PROJECT_NAME} SKIP_COMPILE)

include(GNUInstallDirs)
install(DIRECTORY launch DESTINATION ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME})
install(DIRECTORY rviz DESTINATION ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME})
install(DIRECTORY urdf DESTINATION ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME})

# Package
ament_package()
create_debian_package()
