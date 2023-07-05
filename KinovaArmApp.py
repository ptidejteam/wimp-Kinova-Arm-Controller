##
# Arm Driver : send a set of commands to the robot 
#
# This code shows how the Arm Controller API is used 
#
# @autor el hachemi Alikacem
#
##

from armController.ArmController import ArmController 
from armController.ScanRobot  import ScanRobot 
from armController.CartesianPosition import CartesianPosition 
from armController.TwistValues import TwistValues 
from armController.JointSpeedValues import JointSpeedValues

from armController.GripperLowlevelControl import GripperLowlevelControl
from armController.NotificationHandler import NotificationHandler, ACTION_NOTIF, ARM_STATE_NOTIF , CONFIG_CHANGE_NOTIF
from armController.ActionSequence import ActionSequence 
from armController.JointAnglesValues import JointAnglesValues
from armController.ArmAction import Move2HomePositionAction, Move2PredefinedPositionAction, Move2CartesianPositionAction,\
    JointTwistAction, Move2PositionAnglesAction, JointSpeedAction

import time ; 

# WHAT IS FOR ... 
# TO REMOVE 
#def sequence_sexamples(armController) : 
#    #armControlle
#    pass 

## -----------------------------------------------------------------------
#  
## -----------------------------------------------------------------------
def main() : 
    # First operation : Creation of the ArmController Instance - creation of the connection and a start a session
    armController = ArmController() 
    
    # Section Notifications ------------------------------------------------- Start 
    # Notifications 
    # Initiates the notification Handling 
    notif_handler = NotificationHandler(armController.get_base_client()) 

    # Subsribe to All (the thirteen) notification types 
    # notif_handler.subscribeAll() 

    # Or : subsribe for a given set of Notification types - See NotificationHandler.py for the defined notification types
    #notif_handler.subscribe_list([ACTION_NOTIF, ARM_STATE_NOTIF , CONFIG_CHANGE_NOTIF ]) 
    # ========================================================================= End

 

    # Device scanning --------------------------------------------------------- START 
    scanRobot = ScanRobot(armController) 
    #scanRobot.scan_devices() 
    # ========================================================================= End


    # Move to Home Position --------------------------------------------------- START 
    home_position = Move2HomePositionAction() 
    armController.perform(home_position)
    # ========================================================================= End



    # Display catesian position ---------------------------------------------- Start
    # Returns (X, Y, Z, Theta_X, Theta_Y , Theta_Z)
    curr_cart_position = armController.read_cartesian_position()
    curr_cart_position.display()
    # ========================================================================= End




    # Move to Predefined Position : Packaging, Home or Zero ------------------- START 
    predef_position = Move2PredefinedPositionAction("Packaging")    
    #armController.perform(predef_position)
    # ========================================================================= End


    # Move to cartesian position ----------------------------------------------- START 
    cart_position = CartesianPosition(0.5 , 0.1 , 0.5)
    cart_pos_action = Move2CartesianPositionAction(cart_position)
    #armController.perform(cart_pos_action)
    # ========================================================================= End

    ## Changer le nom - TODO 

    ## Joint Twist Action ------------------------------------------------------ START
    twistValues = TwistValues(0.03 , 0 , 0 , 0 , 0 , 0) # move on X, 3cm by second 
    duration = 3 
    twist_action = JointTwistAction(twistValues , duration)
    #armController.perform(twist_action)
    # ========================================================================= End


    ## Rotate joints to the given angle ---------------------------------------- START
    jointAnglesValues = JointAnglesValues(0,0,0,0,0,90,45)
    positionAngle_action = Move2PositionAnglesAction(jointAnglesValues) 
    # armController.perform(positionAngle_action)
    # ========================================================================= End


    ## Rotate joints to the given angle ---------------------------------------- START
    jointSpeedValues = JointSpeedValues(0 , 5 , 0 , 0 , 0 , 0, -20) #
    duration = 3 
    jointSpeedAction = JointSpeedAction(jointSpeedValues, duration)
    armController.perform(jointSpeedAction) 
    # ========================================================================= End



    # Start ------------------------------------------------------ Read the current poisiton 
    # Returns (X, Y, Z,Theta_X, Theta_Y , Theta_Z)
    curr_cart_position = armController.read_cartesian_position()
    curr_cart_position.display()
    # END ====================================================== Read the current poisiton 
     

    #
    # Start ------------------------------------------------------ Read the current poisiton 
    gripperllControl = GripperLowlevelControl(armController) 
    #gripperllControl.reachGripperPosition(0)
    time.sleep(1)

    #gripperllControl.reachGripperPosition(50)
    time.sleep(1)

    #gripperllControl.reachGripperPosition(100)
    #time.sleep(1)
     
    # ---------------------------
    #gripperllControl.reachGripperPosition(0)
    # Juste a pause 
    #time.sleep(1)

    # Very important : terminate() must be called when the gripper manipulation 
    # is terminated before doing other actions on the robot 
    #gripperllControl.terminate() 

    #
    # Start ------------------------------------------------------ Read the current poisiton 


    # Start ------------------------------------------------------ Read the current poisiton 
    # Create a sequence 
    
    #action_sequence = ActionSequence("Sequence Gripper" , armController.get_base_cyclic_client()) 
    #action_sequence.add_cartesian_action(CartesianPosition(0.4 , 0 , 0.6) , 0 ) ;
    #action_sequence.add_cartesian_action(CartesianPosition(0.4 , 0.1 , 0.55) , 1) ;
    #action_sequence.add_cartesian_action(CartesianPosition(0.6 , 0.1 , 0.55) , 1) ;    
    #action_sequence.add_cartesian_action(CartesianPosition(0.4 , 0 , 0.5 , 90 , 45 , None  ) , 2) ;
    #armController.play_sequence(action_sequence)
    
    # -- Finalisation du code  ----------------------------
    # Unsubscribe for all notification   
    notif_handler.unsubscribe() 

    # Ends the sessions and deconnection of the client
    armController.disconnect() 


## --------------------------------------------------------------
if __name__ == "__main__":
    exit(main())