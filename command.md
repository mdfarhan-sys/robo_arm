
cd ~/robo_arm
colcon build --symlink-install
source install/setup.bash

# Terminal 1: Gazebo world + spawn
ros2 launch pick_place_demo gz_pick_place.launch.py

# Terminal 2: robot_state_publisher + MoveIt (Panda config)
ros2 launch moveit_resources_panda_moveit_config demo.launch.py

# Terminal 3: run the pick-and-place sequence
ros2 run pick_place_demo pick_place_node
