## 
#  Main Class implementing Connection and control of the arm 
# 
# This Code uses some snipets from Examples provides by Kinova 
#
#
# @author : El hachemi Alikacem 
# @date : 10 June 2023
#
## -----------------------------------------------------------------------


# from asyncio.windows_events import NULL  - to remove 

import threading  
import time 

from kortex_api.TCPTransport import TCPTransport
from kortex_api.UDPTransport import UDPTransport
from kortex_api.RouterClient import RouterClient, RouterClientSendOptions
from kortex_api.SessionManager import SessionManager
from kortex_api.autogen.messages import Session_pb2
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.messages import Base_pb2
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient

from armController.ConstantsUtilities import DISCONNECT, NOT_CONNECTED, CARTESIAN_MV_ACTION, \
     READ_CART_VALUES, TWIST_CMD, JOINT_SPEED_CMD, MOVE_TO_POSITION_ANGLES

from armController.CartesianPosition import CartesianPosition

##
# Global Variables : 
IP_ADRESSE = "192.168.0.10"   # IP Adresse of the ARM
USERNAME = "admin"            # username and password : used to create a session
PWD = "admin"
TCP_PORT = 10000              # TCP Port : used for high level control 
UDP_PORT = 10001              # UDP Port : used for low  level control 
TRACE = True                  # Boolean enabling/desabling trace printing 
SESSION_INACTIVITY_TIMEOUT    = 60000 # (milliseconds)
CONNECTION_INACTIVITY_TIMEOUT = 2000  # (milliseconds)
#
## 
TIMEOUT_DURATION = 20
##
#
#
errorCallback = lambda kException: print("_________ callback error _________ {}".format(kException))

class ArmController :
    
    ## ----------------------------------------------------------
    # Constructor 
    def __init__(self) : 
        self.connected = False      # Indicate if the client is connected to the robot 
        self.busy = False           # Indicate if the robot is busy or not 
        self.transport = TCPTransport()
        self.router = RouterClient(self.transport , errorCallback) 
        self.transport.connect(IP_ADRESSE, TCP_PORT)
        self.connected = True
        self.new_session()
        self.base_client =  BaseClient(self.router)
        self.base_cyclic_client = BaseCyclicClient(self.router)

        if (TRACE == True) : 
            print("[INFO-",__name__ ,"] " , self.msg_connect_data()) ; 

    ## --------------------------------------------------------------
    #
    def msg_connect_data(self): 
        msg = "Connected to: " + IP_ADRESSE + " ON TCP Port:" + str(TCP_PORT) + " As: " + str(USERNAME )
        return msg


    ##
    # Getter : returns the router Client Object if connected to the Robot 
    def get_router(self) :
        if (self.connected == True) : 
            return self.router 
        else : 
            return None

    ## ---------------------------------------------------------------
    #
    #
    ##
    def get_base_cyclic_client(self) : 
        if (self.connected == True) : 
            return self.base_cyclic_client  
        else : 
            return None

    ## --------------------------------------------------------------
    # Create a new session 
    #Should I check if there is connected first ?
    def new_session(self) :

        session_info = Session_pb2.CreateSessionInfo()
        session_info.username = USERNAME
        session_info.password = PWD
        session_info.session_inactivity_timeout = SESSION_INACTIVITY_TIMEOUT   # (milliseconds)
        session_info.connection_inactivity_timeout = CONNECTION_INACTIVITY_TIMEOUT # (milliseconds)

        self.session = SessionManager(self.router)
        self.session.CreateSession(session_info)

    ## ----------------------------------------------------------
    # Disconnect the client 
    # Terminates the session and close the connexion 
    def disconnect(self) : 
        if (self.connected == True) :
            self.session.CloseSession() 
            self.transport.disconnect()
            self.connected = False 
            if (TRACE== True) : 
                print ("[INFOS]" , DISCONNECT)                
        else : 
            if (TRACE== True) : 
                print ("[WARN]" , NOT_CONNECTED)
        # to be completed

    ## ----------------------------------------------------------
    # Return True or False whether the client is connected or not 
    def isConnected(self) :
        return self.connected 


    ## ----------------------------------------------------------
    # Move the Arm to a given catesian position 
    ## ----------------------------------------------------------
    def move_to_Home_position(self) : 
        self.move_to_predefined_position("Home") 
        
    ## -----------------------------------------------------------
    # Create closure to set an event after an END or an ABORT
    ## ----------------------------------------------------------
    def check_for_end_or_abort(self, e):
        """Return a closure checking for END or ABORT notifications

            Arguments:
            e -- event to signal when the action is completed
            (will be set when an END or ABORT occurs)
        """
        print("Notification Call Back")
        def check(notification, e = e):
            print("EVENT : " + Base_pb2.ActionEvent.Name(notification.action_event))
            if notification.action_event == Base_pb2.ACTION_END \
            or notification.action_event == Base_pb2.ACTION_ABORT:                
                e.set()
        return check
 

    ## ----------------------------------------------------------
    # Move the Arm to a given catesian position 
    # Predefined Positions (API. V2.3): Home, Packaging, Zero 
    ## ----------------------------------------------------------
    def move_to_predefined_position(self, positionLabel) : 
        # Make sure the arm is in Single Level Servoing mode
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        self.base_client.SetServoingMode(base_servo_mode)
    
        # Move arm to ready position
        print("Moving the arm to a safe position")
        action_type = Base_pb2.RequestedActionType()
        action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
        action_list = self.base_client.ReadAllActions(action_type)
        action_handle = None
        for action in action_list.action_list:            
            if action.name == positionLabel :
                action_handle = action.handle

        if action_handle == None:
            print("Can't reach safe position. Exiting") # CHANGER LE MESSAGE  
            return False

        e = threading.Event()
        notification_handle = self.base_client.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        self.base_client.ExecuteActionFromReference(action_handle)
        finished = e.wait(TIMEOUT_DURATION)
        self.base_client.Unsubscribe(notification_handle)

        if finished:
            print("Safe position reached")
        else:
            print("Timeout on action notification wait")
        return finished
    
    ## ----------------------------------------------------------
    #
    #
    #
    ## ----------------------------------------------------------
    def read_cartesian_position(self) :
        if (self.connected == True) : 
            if (TRACE == True) : 
                print ("[INFO]" , READ_CART_VALUES)

            action = Base_pb2.Action()
            action.name = "Read Cartesian Data"
            action.application_data = ""

            feedback = self.base_cyclic_client.RefreshFeedback()

            # cartesian_pose = action.reach_pose.target_pose

            x = feedback.base.tool_pose_x     # (meters)
            y = feedback.base.tool_pose_y     # (meters)
            z = feedback.base.tool_pose_z     # (meters)
            theta_x = feedback.base.tool_pose_theta_x # (degrees)
            theta_y = feedback.base.tool_pose_theta_y # (degrees)
            theta_z = feedback.base.tool_pose_theta_z # (degrees) 

            cartesianPosition = CartesianPosition(x,y,z,theta_x , theta_y , theta_z) 
            return cartesianPosition

        else : 
            if (TRACE == True) : 
                print ("[WARN]" , NOT_CONNECTED)
            return None


 
    ## ----------------------------------------------------------
    # Move the Arm to a given catesian position 
    #
    # @param catesianPosition : data object contains x, y, z, theta_x, theta_y and theta_z
    ## -----------------------------------------------------------
    def move_to_cartesian( self , cartesianPosition ) : 
        if (self.connected == True) : 
            if (TRACE == True) : 
                print ("[Info]" , CARTESIAN_MV_ACTION)

            # Get the values from the instance (parametre)
            x = cartesianPosition.pos_x
            y = cartesianPosition.pos_y
            z = cartesianPosition.pos_z
            ang_x = cartesianPosition.theta_x 
            ang_y = cartesianPosition.theta_y 
            ang_z = cartesianPosition.theta_z 

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

            # for debuging
            print("Moving to : " , x , y, z , ang_x, ang_y , ang_z)

            cartesian_pose = action.reach_pose.target_pose
            cartesian_pose.x = x    # (meters)
            cartesian_pose.y = y    # (meters)
            cartesian_pose.z = z    # (meters)
            cartesian_pose.theta_x = ang_x  # (degrees)
            cartesian_pose.theta_y = ang_y  # (degrees)
            cartesian_pose.theta_z = ang_z  # (degrees)


            e = threading.Event()
            notification_handle = self.base_client.OnNotificationActionTopic(
                self.check_for_end_or_abort(e),
                Base_pb2.NotificationOptions()
            )

            print("Executing action")
            self.base_client.ExecuteAction(action)

            print("Waiting for movement to finish ...")
            finished = e.wait(TIMEOUT_DURATION)
            self.base_client.Unsubscribe(notification_handle)

            if finished:
                print("Cartesian movement completed")
            else:
                print("Timeout on action notification wait")
        
        else :
            if (TRACE == True) : 
                print ("[WARN]" , NOT_CONNECTED)

                 
                 
       
    ## ----------------------------------------------------------
    #  TO REVIEW 
    #
    ## ----------------------------------------------------------
    def move_to_position_angles(self , angles):
        # check if connected to the robot 
        if (self.connected == False) : 
            if (TRACE == True) : 
                 print ("[WARN]" , NOT_CONNECTED)

            return False
        
        # Client connected to the robot 
        if (TRACE == True) : 
                print ("[Info]" , MOVE_TO_POSITION_ANGLES)

             # Make sure the arm is in Single Level Servoing mode
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        self.base_client.SetServoingMode(base_servo_mode)
    
        # Move arm to ready position
        constrained_joint_angles = Base_pb2.ConstrainedJointAngles()

        actuator_count = self.base_client.GetActuatorCount().count
        print("Nombre Actuators : " , actuator_count)
        #angles = [0.0] * actuator_count
        #print ("Angles : " , angles )
        # Actuator 4 at 90 degrees
        for joint_id in range(len(angles)):
            joint_angle = constrained_joint_angles.joint_angles.joint_angles.add()
            print("Joint ID : " , joint_id , "  Angle : " , angles[joint_id]) 
            joint_angle.joint_identifier = joint_id
            joint_angle.value = angles[joint_id]
        
        e = threading.Event()
        notification_handle = self.base_client.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        print("Reaching joint angles...")
        self.base_client.PlayJointTrajectory(constrained_joint_angles)

        print("Waiting for movement to finish ...")
        finished = e.wait(TIMEOUT_DURATION)
        self.base_client.Unsubscribe(notification_handle)

        if finished:
            print("Joint angles reached")
        else:
            print("Timeout on action notification wait")
        return finished

    ## ----------------------------------------------------------
    #
    ## ----------------------------------------------------------
    def twist_command(self, twistValues , duration):
        if (self.connected == True) : 
            if (TRACE == True) : 
                print ("[Info]" , TWIST_CMD)


            # Creation de l'objet twist Command
            command = Base_pb2.TwistCommand()

            # Initialisation de l'objet 
            command.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_TOOL
            command.duration = 0
        
            twist = command.twist
            twist.linear_x = twistValues.linear_x 
            twist.linear_y = twistValues.linear_y
            twist.linear_z = twistValues.linear_z 
            twist.angular_x = twistValues.angular_x 
            twist.angular_y = twistValues.angular_y 
            twist.angular_z = twistValues.angular_z 

            print ("Sending the twist command for ", duration , " seconds...")
            self.base_client.SendTwistCommand(command)

            # Let time for twist to be executed
            time.sleep(duration) 

            print ("Stopping the robot...")
            self.base_client.Stop()
            time.sleep(1)

            return True
        else : 
            if (TRACE == True) : 
                print ("[WARN]" , NOT_CONNECTED)
            return False 
    
    ## ----------------------------------------------------------
    # Set the speed for each actuator 
    # Note that the command is a setup of a value (for a device, here the Joint) 
    # So the command is excuted "continuesly" unless a stop is sent to the robot.
    # The client (program) should wait until the command is terminated.
    #
    ## ----------------------------------------------------------
    def joint_speed_command(self, jointSpeedValues , duration):

        # check if connected to the robot 
        if (self.connected == False) : 
            if (TRACE == True) : 
                 print ("[WARN]" , NOT_CONNECTED)

            return False
        
        # Client connected to the robot 
        if (TRACE == True) : 
                print ("[Info]" , JOINT_SPEED_CMD)


        joint_speeds = Base_pb2.JointSpeeds()
        actuator_count = self.base_client.GetActuatorCount().count

        # The 7DOF robot will spin in the same direction for 10 seconds
        # print ("Number of actuators : " , actuator_count)
        if actuator_count == 7:
            # speeds = [SPEED, 0, -SPEED, 0, SPEED, 0, -SPEED]
            i = 0
        speeds = jointSpeedValues.get_speedValues() 
        for speed in speeds:
            print ("Actuator " , i , " - Speed : " , speed )
            joint_speed = joint_speeds.joint_speeds.add()
            joint_speed.joint_identifier = i 
            joint_speed.value = speed
            joint_speed.duration = 0
            i = i + 1
        
        print ("Sending the joint speeds for 10 seconds...")
        self.base_client.SendJointSpeedsCommand(joint_speeds)
        time.sleep(duration) # 10seconds 

        print ("Stopping the robot")
        self.base_client.Stop()

        return True


# Liste des operations : 
#   - Faire un Scan low level 
#   - Goto Predefined position 
#   - Goto the predefined Position : HOME 
#   - Display Cartesian position

#   - Wait the robot finishing an action 
#   - Stop the robot 
#   - Handling notification : See 8h30 (video) 

# TODO :
#   - Create and Play a sequence 
    