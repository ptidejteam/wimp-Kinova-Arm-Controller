##
# Arm Driver : send a set of commands to the robot 
#
# This code shows how the Arm Controller API is used 
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
    JointTwistAction
import time ; 

# WHAT IS FOR ... 
# TO REMOVE 
#def sequence_sexamples(armController) : 
#    #armControlle
#    pass 

def main() : 
    # First operation : Creation of the ArmController Instance - creation of the connection and a start a session
    armController = ArmController() 
    
    # ------------------------------------------------------ Section Notifications : Start 
    # Notifications 
    # Initiates the notification Handling 
    notif_handler = NotificationHandler(armController.get_base_client()) 

    # Subsribe to All (the thirteen) notification types 
    # notif_handler.subscribeAll() 

    # Or : subsribe for a given set of Notification types 
    #notif_handler.subscribe_list([ACTION_NOTIF, ARM_STATE_NOTIF , CONFIG_CHANGE_NOTIF ]) 

    # ================================================================= Notifications : End

     

    home_position = Move2HomePositionAction()     
    #armController.perform(home_position)

    curr_cart_position = armController.read_cartesian_position()
    curr_cart_position.display()

    ## ----------
    

    #cart_position = CartesianPosition(None , None , None , 90 , 0  , 70)
    #cart_pos_action = Move2CartesianPositionAction(cart_position)
    #armController.perform(cart_pos_action)
    curr_cart_position = armController.read_cartesian_position()
    #curr_cart_position.display()



    #jointAnglesValues = JointAnglesValues(0,0,0,45,180,0,90)
    #armController.move_to_position_angles(jointAnglesValues) 

    #jointAnglesValues = JointAnglesValues(0,0,0,0,0,0,0)
    #armController.move_to_position_angles(jointAnglesValues) 

    jointAnglesValues = JointAnglesValues(280,15,0,140,0,300,270)
    armController.move_to_position_angles(jointAnglesValues) 


    cart_position = CartesianPosition( 0.20 , 0.43  , 0.20)
    cart_pos_action = Move2CartesianPositionAction(cart_position)
    #armController.perform(cart_pos_action)
    curr_cart_position = armController.read_cartesian_position()
    curr_cart_position.display()



    #armController.perform(cart_pos_action)

    #cart_position = CartesianPosition(None , None , 0.15)
    #cart_pos_action = Move2CartesianPositionAction(cart_position)
    #armController.perform(cart_pos_action)
    curr_cart_position = armController.read_cartesian_position()
    curr_cart_position.display()

    ## ===================================================================
    # cart_position = CartesianPosition(0.11 , 0.67 , 0.14 , -90 , -177 , 20)
    # armController.perform(cart_pos_action)



    #cart_position = CartesianPosition(None , 0.05 , None)
    #armController.perform(cart_pos_action)

    curr_cart_position = armController.read_cartesian_position()
    #curr_cart_position.display()


    # Start ------------------------------------------------------ Section Move to Predefined position : Start 
    # Move the predefined 'home' position 
    # armController.move_to_Home_position() 

    # Moving to the predefined 'Packaging' position - Zero is also a predefined position
    #armController.move_to_predefined_position("Packaging")   #Zero 
    # ====================================================== Section Move to Predefined position : End 



    # Start ------------------------------------------------------ Section to cartesian position : Start 
    # (X, Y, Z) = (0.5 , 0.1 , 0.5)
    #cart_position = CartesianPosition(0.5 , 0.1 , 0.5)
    #armController.move_to_cartesian(cart_position)
     
    # (X, Y, Z) = (Current X , Current Y , 0.5)
    #cart_position = CartesianPosition(None , None , 0.55)
    #armController.move_to_cartesian(cart_position)

    # Here, we specify the position of the arm for a given theta_X, theta_Y tetha_Z

    # (theta_X, theta_Y tetha_Z) = (90 , 0 , 45)  degrees 
    # Note that (X, Y and Z) = (current X, current Y and current Z) 

    #cart_position = CartesianPosition(None , None , None, 90 , 0 , 45)
    #armController.move_to_cartesian(cart_position)
    # END ====================================================== Section to cartesian position


    # Start ------------------------------------------------------ Read the current poisiton 
    # Returns (X, Y, Z,Theta_X, Theta_Y , Theta_Z)
    #curr_cart_position = armController.read_cartesian_position()
    #curr_cart_position.display()
    # END ====================================================== Read the current poisiton 
     


    # Start ------------------------------------------------------ Read the current poisiton 
    duration = 3 # seconds 
    twistValues = TwistValues(0.03 , 0 , 0 ) 
    twistValues = TwistValues(0.03 , 0 , 0 , 0 , 0 , 0) 
    #armController.twist_command(twistValues , duration)

    # END ====================================================== Read the current poisiton 


    # ---------------------------
    # Start ------------------------------------------------------ Read the current poisiton 
    # Sending joint_speed_command
    jointSpeedValues = JointSpeedValues(5 , 0 , 0 , 0 , 0 , 0, -20) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)


    #
    # Start ------------------------------------------------------ Read the current poisiton 

    #gripperllControl = GripperLowlevelControl(armController) 
    #gripperllControl.reachGripperPosition(0)
    #time.sleep(1)

    #gripperllControl.reachGripperPosition(50)
    #time.sleep(1)

    #gripperllControl.reachGripperPosition(100)
    #time.sleep(1)

    # ---------------------------
    #gripperllControl.reachGripperPosition(0)
    #time.sleep(1)
    #gripperllControl.terminate() 

    #
    # Start ------------------------------------------------------ Read the current poisiton 

    # Sending joint_speed_command
    # ---------------------------
    jointSpeedValues = JointSpeedValues(5 , 0 , 0 , 0 , 0 , 0, 0) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)

    #
    # Start ------------------------------------------------------ Read the current poisiton 

    # ---------------------------
    #gripperllControl = GripperLowlevelControl(armController) 
    
    #gripperllControl.reachGripperPosition(100)
    
    #time.sleep(1)
    #gripperllControl.terminate() 


    # Start ------------------------------------------------------ Read the current poisiton 
    jointSpeedValues = JointSpeedValues(5 , 0 , 0 , 0 , 0 , 0, 0) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)
    
    # Start ------------------------------------------------------ Read the current poisiton 
    jointAnglesValues = JointAnglesValues(0,0,0,0,0,90,45)
    #armController.move_to_position_angles(jointAnglesValues) 


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