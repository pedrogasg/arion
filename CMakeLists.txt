cmake_minimum_required(VERSION 2.8.3)
project(arion)

find_package(catkin REQUIRED COMPONENTS message_generation rospy)

catkin_python_setup()


catkin_package(
  CATKIN_DEPENDS message_runtime
)

catkin_install_python(PROGRAMS 
  bin/predict_stearing
  bin/move_position
  bin/camera
  bin/path_viz
  bin/move_actuator
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})