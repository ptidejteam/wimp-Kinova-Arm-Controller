##
# Arm Driver : send a set of command to the robot 
#
#
#
#
##
from armController.ArmController import ArmController 
from armController.ScanRobot  import ScanRobot 
from armController.CartesianPosition import CartesianPosition 
from armController.TwistValues import TwistValues 
from armController.JointSpeedValues import JointSpeedValues

from armController.GripperLowlevelControl import GripperLowlevelControl ;

import time ; 

def main() : 
    armController = ArmController() 
    
    # Send the Robot the predefined Home position 
    armController.move_to_Home_position()

    # Send the Robot the predefined position named "Packaging"
    #armController.move_to_predefined_position("Packaging")   #Zero 

    #scanRobot = ScanRobot(armController) 
    #scanRobot.scan_devices() 

    cart_position = CartesianPosition(0.5 , 0 , 0.5)
    armController.move_to_cartesian(cart_position)

    #cart_position = CartesianPosition(None , None , 0.55)
    #armController.move_to_cartesian(cart_position)

    #cart_position = CartesianPosition(0.5 , 0 , 0.55)
    #armController.move_to_cartesian(cart_position)

    cart_position = CartesianPosition(None , None , None, 60 , 0 , 90)
    #armController.move_to_cartesian(cart_position)

    #curr_cart_position = armController.read_cartesian_position()
    #curr_cart_position.display()

    #armController.twist_command(0.03, 0.03, 0, 0, 0, 0, 4) 
    duration = 3 # seconds 
    #twistValues = TwistValues(0.03 , 0 , 0 ) 

    #twistValues = TwistValues(0.03 , 0 , 0 , 0 , 0 , 5 ) 
    #armController.twist_command(twistValues , duration)


    # Sending joint_speed_command
    #jointSpeedValues = JointSpeedValues([5 , 0 , 0 , 0 , 0 , 0, 0]) 
    duration = 3 
    #armController.joint_speed_command(jointSpeedValues , duration)


    #
    armController.UDPConnexion() 
    gripperllControl = GripperLowlevelControl(armController.router, armController.routerUDP , 
                                              armController.base_client) 
    gripperllControl.reachGripperPosition(0)
    time.sleep(1)
    gripperllControl.reachGripperPosition(50)
    time.sleep(1)

    gripperllControl.reachGripperPosition(100)
    time.sleep(1)
    gripperllControl.reachGripperPosition(0)

    #
    
    # Ends the sessions and deconnection of the client
    armController.disconnect() 
## --------------------------------------------------------------
if __name__ == "__main__":
    exit(main())