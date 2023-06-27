##
# Arm Driver : send a set of commands to the robot 
#
#
##
from armController.ArmController import ArmController 
from armController.ScanRobot  import ScanRobot 
from armController.CartesianPosition import CartesianPosition 
from armController.TwistValues import TwistValues 
from armController.JointSpeedValues import JointSpeedValues

from armController.GripperLowlevelControl import GripperLowlevelControl
from armController.NotificationHandler import NotificationHandler 
from armController.ActionSequence import ActionSequence 
from armController.JointAnglesValues import JointAnglesValues

import time ; 

def sequence_sexamples(armController) : 

    #armControlle
    pass 

def main() : 
    armController = ArmController() 
    
    notif_handler = NotificationHandler(armController.get_base_client()) 
    notif_handler.subscribeAll() 



    # Send the Robot the predefined Home position 
    #armController.move_to_Home_position() 

    #notif_handler.subscribe() 
    # Send the Robot the predefined position named "Packaging"
    #armController.move_to_predefined_position("Packaging")   #Zero 

    #scanRobot = ScanRobot(armController) 
    #scanRobot.scan_devices() 

    cart_position = CartesianPosition(0.5 , 0.1 , 0.5)
    #armController.move_to_cartesian(cart_position)

    #cart_position = CartesianPosition(None , None , 0.55)
    #armController.move_to_cartesian(cart_position)

    cart_position = CartesianPosition(0.5 , 0.1 , 0.5)
    #armController.move_to_cartesian(cart_position)

    cart_position = CartesianPosition(None , None , None, 90 , 0 , 45)
    #armController.move_to_cartesian(cart_position)

    #curr_cart_position = armController.read_cartesian_position()
    #curr_cart_position.display()


    duration = 3 # seconds 

    twistValues = TwistValues(0.03 , 0 , 0 ) 

    twistValues = TwistValues(0.03 , 0 , 0 , 0 , 0 , 0) 
    #armController.twist_command(twistValues , duration)


    # Sending joint_speed_command
    jointSpeedValues = JointSpeedValues(5 , 0 , 0 , 0 , 0 , 0, -20) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)


    #
    #armController.UDPConnexion() 
    #gripperllControl = GripperLowlevelControl(armController.router, armController.routerUDP , armController.base_client) 

    #gripperllControl = GripperLowlevelControl(armController) 
    #gripperllControl.reachGripperPosition(0)
    #time.sleep(1)

    #gripperllControl.reachGripperPosition(50)
    #time.sleep(1)

    #gripperllControl.reachGripperPosition(100)
    #time.sleep(1)

    #gripperllControl.reachGripperPosition(0)
    #time.sleep(1)
    #gripperllControl.terminate() 

    #
    
    # Sending joint_speed_command
    jointSpeedValues = JointSpeedValues(5 , 0 , 0 , 0 , 0 , 0, 0) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)

    #
    gripperllControl = GripperLowlevelControl(armController) 
    print ("LL commande to the gripper - start ")
    gripperllControl.reachGripperPosition(100)
    print ("LL commande to the gripper - end ")
    time.sleep(1)
    gripperllControl.terminate() 


    jointSpeedValues = JointSpeedValues(5 , 0 , 0 , 0 , 0 , 0, 0) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)

    cart_position = CartesianPosition(0.5 , 0 , 0.60)
    #armController.move_to_cartesian(cart_position)


    jointAnglesValues = JointAnglesValues(0,0,0,0,0,90,45)
    #armController.move_to_position_angles(jointAnglesValues) 


    # Create a sequence 
    
    #action_sequence = ActionSequence("Sequence Gripper" , armController.get_base_cyclic_client()) 
    #action_sequence.add_cartesian_action(CartesianPosition(0.4 , 0 , 0.6) , 0 ) ;
    #action_sequence.add_cartesian_action(CartesianPosition(0.4 , 0.1 , 0.55) , 1) ;
    #action_sequence.add_cartesian_action(CartesianPosition(0.6 , 0.1 , 0.55) , 1) ;    
    
    #action_sequence.add_cartesian_action(CartesianPosition(0.4 , 0 , 0.5 , 90 , 45 , None  ) , 2) ;

    #armController.play_sequence(action_sequence)
    

    # Unsubscribe for all notification   
    notif_handler.unsubscribe() 

    # Ends the sessions and deconnection of the client
    armController.disconnect() 
## --------------------------------------------------------------
if __name__ == "__main__":
    exit(main())