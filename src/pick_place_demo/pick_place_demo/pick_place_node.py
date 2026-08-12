import rclpy
from moveit.planning import MoveItPy
from geometry_msgs.msg import PoseStamped

def make_pose(x, y, z, w=1.0):
    p = PoseStamped()
    p.header.frame_id = "panda_link0"
    p.pose.position.x = x
    p.pose.position.y = y
    p.pose.position.z = z
    p.pose.orientation.w = w
    return p

def move_to(arm, pose):
    arm.set_goal_state(pose_stamped_msg=pose, pose_link="panda_link8")
    plan = arm.plan()
    if plan:
        arm.execute()
    else:
        print("Planning failed for target pose")

def main():
    rclpy.init()
    panda = MoveItPy(node_name="pick_place_node")
    arm = panda.get_planning_component("panda_arm")
    gripper = panda.get_planning_component("hand")

    # Pre-grasp: above the box at (0.5, 0, 0.05)
    move_to(arm, make_pose(0.5, 0.0, 0.25))
    # Descend
    move_to(arm, make_pose(0.5, 0.0, 0.12))
    # Close gripper
    gripper.set_goal_state(configuration_name="close")
    if gripper.plan():
        gripper.execute()
    # Lift
    move_to(arm, make_pose(0.5, 0.0, 0.3))
    # Move to drop location
    move_to(arm, make_pose(0.2, 0.4, 0.3))
    move_to(arm, make_pose(0.2, 0.4, 0.15))
    # Open gripper
    gripper.set_goal_state(configuration_name="open")
    if gripper.plan():
        gripper.execute()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
