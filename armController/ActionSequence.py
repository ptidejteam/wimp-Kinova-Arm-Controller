##
# Managing a sequence of actions 
# Should be used to create a sequence of actions, then given as a parameter to ArmController to play the sequence 
#
#
#
# @author : El hachemi Alikacem 
# @date : 19 June 2023
#
##

from kortex_api.autogen.messages import Session_pb2, Base_pb2

import threading 

class ActionSequence : 
    def __init__(self , _seqName , _base_cyclic_client ) : 
        print("Creating Sequence")
        self.sequence = Base_pb2.Sequence()
        self.sequence.name = _seqName 
        self.base_cyclic_client = _base_cyclic_client 
   
    def get_sequence(self) : 
        return self.sequence 
    ##
    #
    ##
    def add_cartesian_action(self, _cartesian_position , _grp_id ) : 
        # create the cart
        # cartesian_action = self.create_cartesian_action() 

        x = _cartesian_position.pos_x
        y = _cartesian_position.pos_y
        z = _cartesian_position.pos_z
        ang_x = _cartesian_position.theta_x 
        ang_y = _cartesian_position.theta_y 
        ang_z = _cartesian_position.theta_z 

        e = threading.Event()
        # Creation an Action 
        action = Base_pb2.Action()
        action.name = "Cartesian action movement"
        action.application_data = ""

        feedback = self.base_cyclic_client.RefreshFeedback()

        #Check if one the values is None, in this case, the arm will keep its
        # current value 

        if (x == None) : 
            x = feedback.base.tool_pose_x # Current pose_x value of the arm 

        if (y == None) : 
            y = feedback.base.tool_pose_y # Current pose_y value of the arm 

        if (z == None) : 
            z = feedback.base.tool_pose_z # Current pose_z value of the arm 

        if (ang_x == None) :                 
            ang_x = feedback.base.tool_pose_theta_x # Current theta_x value of the arm 

        if (ang_y == None) :                 
            ang_y = feedback.base.tool_pose_theta_y # Current theta_y value of the arm 

        if (ang_z == None) :                 
            ang_z = feedback.base.tool_pose_theta_z # Current theta_z value of the arm 

        cartesian_pose = action.reach_pose.target_pose
        cartesian_pose.x = x    
        cartesian_pose.y = y    
        cartesian_pose.z = z    
        cartesian_pose.theta_x = ang_x  
        cartesian_pose.theta_y = ang_y  
        cartesian_pose.theta_z = ang_z  

        # Creation of a task 
        task = self.sequence.tasks.add()
        task.group_identifier = _grp_id
        task.action.CopyFrom(action)


    def add_angular_action(self , _grp_id  ) : 
        print("Creating angular action")
        angular_action = Base_pb2.Action()
        angular_action.name = "Example angular action"
        angular_action.application_data = ""
    
        actuator_count = base.GetActuatorCount().count
        for joint_id in range(actuator_count):
            joint_angle = angular_action.reach_joint_angles.joint_angles.joint_angles.add()
            joint_angle.value = 0.0

        task = self.sequence.tasks.add()
        task.group_identifier = _grp_id # sequence elements with same group_id are played at the same time
        task.action.CopyFrom(angular_action)