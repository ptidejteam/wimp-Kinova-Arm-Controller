##
#  A set of classes implementing the actions that could be performed on the ARM
##

HOME_POSITION      = 1 
PREDEF_POSITION    = 2 
CARTESIAN_POSITION = 3 
POSITION_ANGLES    = 4
JOINT_TWIST        = 5 
JOINT_SPEED        = 6 

## -
# Implements move 2 HOME Position Action 
##
class Move2HomePositionAction() : 
   
    def action_type(self) : 
        return HOME_POSITION 
    
## ===================================================================
# Implements move 2 predefined Position Action 
## ===================================================================
class Move2PredefinedPositionAction() : 
    def __init__(self, _position_label) : 
        self.position_label = _position_label        

    ##
    #
    ##
    def action_type(self) : 
        return PREDEF_POSITION
    ##
    #
    ##
    def get_position_label(self) : 
        return self.position_label

## ===================================================================
# Implement Move to cartesian position Action 
# one should provide Cartesian Values within Catesian Position Instance
# by using the constructor  
## ===================================================================
class Move2CartesianPositionAction() : 
    def __init__(self , _cartesian_position) : 
        self.cartesian_position = _cartesian_position
        pass

    def action_type(self) : 
        return CARTESIAN_POSITION 
    
    def get_cartesian_position(self) :
        return self.cartesian_position

## ===================================================================
# Each Joint rotates according the angle given as a parametre 
# One should provide 
# by using the constructor  
## ===================================================================
class Move2PositionAnglesAction() : 

    
    def __init__(self , _joint_angles) : 
        self.joint_angles = _joint_angles

    def action_type(self) : 
        return POSITION_ANGLES 

    def get_joint_Angles(self) :
        return self.joint_angles
        

     
## ===================================================================
## ===================================================================
class JointTwistAction() :

    def __init__(self , _twist_values , duration) : 
        self.twist_values = _twist_values
        self.duration = duration 

    def action_type(self) : 
        return JOINT_TWIST 

    def get_duration(self) :
        return self.duration 

    ## --------------------------------------------------------------------
    def get_twist_values(self) : 
        return self.twist_values

## ===================================================================
# Class 
#
## ===================================================================
class JointSpeedAction() : 
    def __init__(self , _joint_speed_values , _duration) : 
        self.joint_speed_values = _joint_speed_values
        self.duration = _duration

    def action_type(self) : 
        return JOINT_SPEED 
    def get_joint_speed_values(self) : 
       return self.joint_speed_values 

    def get_duration(self) : 
        return self.duration 








