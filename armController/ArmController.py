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
from kortex_api.autogen.messages.Base_pb2 import ProtectionZone, CartesianLimitation
from armController.ArmAction import HOME_POSITION, PREDEF_POSITION, CARTESIAN_POSITION, POSITION_ANGLES, JOINT_TWIST, JOINT_SPEED
from google.protobuf import json_format

from armController.ConstantsUtilities import DISCONNECT_MSG, NOT_CONNECTED_MSG, CARTESIAN_MV_ACTION_MSG,\
     READ_CART_VALUES_MSG, TWIST_CMD_MSG, JOINT_SPEED_CMD_MSG, MOVE_TO_POSITION_ANGLES_MSG, MOVE_TO_PREDEFINED_POSITION_MSG,\
     IP_ADRESSE, USERNAME, PWD, TCP_PORT, UDP_PORT, TRACE, SESSION_INACTIVITY_TIMEOUT, CONNECTION_INACTIVITY_TIMEOUT, TIMEOUT_DURATION


from armController.CartesianPosition import CartesianPosition


## --------------------------------------------------------------
#
#
errorCallback = lambda kException: print("_________ callback error _________ {}".format(kException))

class ArmController :
    
    ## ----------------------------------------------------------
    # Constructor 
    #
    ## ----------------------------------------------------------
    def __init__(self) : 
        print ("Connecttion Initalization")
        self.connected = False      # Indicate if the client is connected to the robot 
        self.busy = False           # Indicate if the robot is busy or not 
        self.transport = TCPTransport()
        self.router = RouterClient(self.transport , errorCallback) 
        print ("Start connection : " ,IP_ADRESSE , '  Port : ' , TCP_PORT )

        self.transport.connect(IP_ADRESSE, TCP_PORT)

        print ("Start connection : DONE " )
        self.connected = True
        self.new_session()
        self.base_client =  BaseClient(self.router)
        self.base_cyclic_client = BaseCyclicClient(self.router)

        if (TRACE == True) : 
            print("[INFO-",__name__ ,"] " , self.msg_connect_data()) ; 



    #
    # don't think, this may work 
    # TOREMOVE 
    def protectionZone(self):
        cartesianLimitation = CartesianLimitation()
        cartesianLimitation.translation = 0.0 # float. No IDEA what should the value
        cartesianLimitation.orientation = 0.0 # float. No IDEA what should the value
        
        protectionZone = ProtectionZone()
        protectionZone.name = "One"
        protectionZone.limitations = cartesianLimitation
        
        protectionZoneHandler = self.base_client.CreateProtectionZone(protectionZone)
            
    ## --
    ## TO REMOVE 
    #  checking the existing methods : To Remove 
    ## -- 
    def retro(self): 
        #gripper = 
        self.base_client.GetMeasuredGripperMovement()

        self.base_client.SendGripperCommand()


    ## --------------------------------------------------------------
    # returns a messsage that containt connection data 
    # Mainlly used for printing 
    ## --------------------------------------------------------------
    def msg_connect_data(self): 
        msg = "Connected to: " + IP_ADRESSE + " ON TCP Port:" + str(TCP_PORT) + " As: " + str(USERNAME )
        return msg


    ## --------------------------------------------------------------
    # Getter : returns the router Client Object if connected to the Robot 
    ## --------------------------------------------------------------
    def get_router(self) :
        if (self.connected == True) : 
            return self.router 
        else : 
            return None

    ## --------------------------------------------------------------
    # Getter : returns the base client instance  
    ## --------------------------------------------------------------
    def get_base_client(self) : 
        if (self.connected == True) : 
            return self.base_client 
        else : 
            return None

    ## ---------------------------------------------------------------
    # Getter : returns the base cyclic client  
    ## --------------------------------------------------------------
    def get_base_cyclic_client(self) : 
        if (self.connected == True) : 
            return self.base_cyclic_client  
        else : 
            return None
    
    ## ---------------------------------------------------------------    
    callback1 = lambda kException: print("_________ callback error _________ {}".format(kException))
    ## 


    ## --------------------------------------------------------------
    # Create a new session 
    # Should I check if there is connected first ?
    ## --------------------------------------------------------------
    def new_session(self) :
        if (self.router != None) :
            session_info = Session_pb2.CreateSessionInfo()
            session_info.username = USERNAME
            session_info.password = PWD
            session_info.session_inactivity_timeout = SESSION_INACTIVITY_TIMEOUT   # (milliseconds)
            session_info.connection_inactivity_timeout = CONNECTION_INACTIVITY_TIMEOUT # (milliseconds)

            self.session = SessionManager(self.router)
            self.session.CreateSession(session_info)
        else : 
            print ("[ERR] Cannot creation a session, the router instance is not created yet")

    ## ----------------------------------------------------------
    # Disconnect the client 
    # Terminates the session and close the connexion 
    def disconnect(self) : 
        if (self.connected == True) :
            self.session.CloseSession() 
            self.transport.disconnect()
            self.connected = False 
            if (TRACE== True) : 
                print ("[INFOS]" , DISCONNECT_MSG)                
        else : 
            if (TRACE== True) : 
                print ("[WARN]" , NOT_CONNECTED_MSG)
        # to be completed @TODO
        # Check if gripper should be terminated 

    ## ----------------------------------------------------------
    # Return True or False whether the client is connected or not 
    def isConnected(self) :
        return self.connected 


    ## -----------------------------------------------------------
    # Create closure to set an event after an END or an ABORT
    # (Notification callback)
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
            
            #print ("Event ID : ", notification.event_identifier)

            if notification.action_event == Base_pb2.ACTION_END \
            or notification.action_event == Base_pb2.ACTION_ABORT:                
                e.set()
        return check

    ## ------------------------------------TMP ----------------------------------
    def check_for_end_or_abort_Twist(self, e): 
        """Return a closure checking for END or ABORT notifications

            Arguments:
            e -- event to signal when the action is completed
            (will be set when an END or ABORT occurs)
        """
        print("Notification Call Back Twist")
        def check1(notification, e = e):
            print("In Check")
            print("EVENT : " + Base_pb2.ActionEvent.Name(notification.action_event))
            
            #print ("Event ID : ", notification.event_identifier)

            if notification.action_event == Base_pb2.ACTION_END \
            or notification.action_event == Base_pb2.ACTION_ABORT:                
                e.set()
        return check1
   
    ## ----------------------------------------------------------
    # Create closure to set an event after an END or an ABORT
    # (Notification callback)
    ## ----------------------------------------------------------
    def check_for_sequence_end_or_abort(self, e):
        """Return a closure checking for END or ABORT notifications on a sequence

        Arguments:
        e -- event to signal when the action is completed
        (will be set when an END or ABORT occurs)
        """

        def check(notification, e = e):
            event_id = notification.event_identifier
            task_id = notification.task_index
            if event_id == Base_pb2.SEQUENCE_TASK_COMPLETED:
                print("Sequence task {} completed".format(task_id))
            elif event_id == Base_pb2.SEQUENCE_ABORTED:
                print("Sequence aborted with error {}:{}"\
                    .format(\
                        notification.abort_details,\
                        Base_pb2.SubErrorCodes.Name(notification.abort_details)))
                e.set()
            elif event_id == Base_pb2.SEQUENCE_COMPLETED:
                print("Sequence completed.")
                e.set()
        return check

    ## ----------------------------------------------------------
    # Move the Arm to (predefined) Home position 
    ## ----------------------------------------------------------
    def move_to_Home_position(self) : 
        self.move_to_predefined_position("Home") 
        

    ## ----------------------------------------------------------
    # Move the Arm to a given catesian position 
    # Predefined Positions (API. V2.3): Home, Packaging, Zero 
    ## ----------------------------------------------------------
    def move_to_predefined_position(self, positionLabel) : 

        if (self.connected == False) :
            print("[WARN] Cannot move to position : " , positionLabel ," - " , NOT_CONNECTED_MSG )             
            return 

        if (TRACE== True) : 
            print ("[INFO] " , MOVE_TO_PREDEFINED_POSITION_MSG )
            
        # Make sure the arm is in Single Level Servoing mode
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        self.base_client.SetServoingMode(base_servo_mode)
    
        # Move arm to ready position
        # print("Moving the arm to a safe position")
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
    # get the catesian position of the Robot : x, y , z , theta_x, theta_y and theta_z
    #
    # Returns an Instance of CartesianPosition that contains the position 
    #
    ## ----------------------------------------------------------
    def read_cartesian_position(self) :
        if (self.connected == True) : 
            if (TRACE == True) : 
                print ("[INFO]" , READ_CART_VALUES_MSG)

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
                print ("[WARN]" , NOT_CONNECTED_MSG)
            return None


 
    ## ----------------------------------------------------------
    # Move the Arm to a given catesian position 
    #
    # @param catesianPosition : data object contains x, y, z, theta_x, theta_y and theta_z
    ## -----------------------------------------------------------
    def move_to_cartesian( self , cartesianPosition ) : 
        if (self.connected == True) : 
            if (TRACE == True) : 
                print ("[Info]" , CARTESIAN_MV_ACTION_MSG)

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

            # print("Executing action")
            self.base_client.ExecuteAction(action)

            # print("Waiting for movement to finish ...")
            finished = e.wait(TIMEOUT_DURATION)
            self.base_client.Unsubscribe(notification_handle)

            if finished:
                if (TRACE == True ) : 
                    print("[INFO] - Cartesian movement completed")
            else:
                if (TRACE == True ) : 
                    print("[WARN] - Timeout on action : Cartesian movement")
        
        else :
            if (TRACE == True) : 
                print ("[WARN]" , NOT_CONNECTED_MSG)

                
    ## ----------------------------------------------------------
    #  Set angles to the actuators 
    #  
    #  TO REVIEW 
    #
    ## ----------------------------------------------------------
    def move_to_position_angles(self , jointAnglesValues):
        # check if connected to the robot 
        if (self.connected == False) : 
            if (TRACE == True) : 
                 print ("[WARN]" , NOT_CONNECTED_MSG)

            return False
        
        # Client connected to the robot 
        if (TRACE == True) : 
                print ("[Info]" , MOVE_TO_POSITION_ANGLES_MSG)

        # Make sure the arm is in Single Level Servoing mode
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        self.base_client.SetServoingMode(base_servo_mode)
    
        # Move arm to ready position
        constrained_joint_angles = Base_pb2.ConstrainedJointAngles()

        actuator_count = self.base_client.GetActuatorCount().count
        print("Nombre Actuators : " , actuator_count)
        angles = jointAnglesValues.angleJointList()
        
        print ("Angles : " , angles )
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

        # print("Reaching joint angles...")
        self.base_client.PlayJointTrajectory(constrained_joint_angles)

        #print("Waiting for movement to finish ...")
        finished = e.wait(TIMEOUT_DURATION)
        self.base_client.Unsubscribe(notification_handle)

        if finished:
            print("[INFO] Joint angles reached")
            "Movement to a position defined by the given angles"
        else:
            print("[WARN] Timeout on action : Movement to angle position")
        return finished

    ## ----------------------------------------------------------
    #
    # important note : A command is not an action
    #   One sends the command, the robot executes it "forever", meanwhile, an other command may be sent
    #    and could be stop() commande which is setting 0 for the 6 twist values. 
    ## ----------------------------------------------------------
    def twist_command(self, twistValues , duration):
        if (self.connected == True) : 
            if (TRACE == True) : 
                print ("[Info]" , TWIST_CMD_MSG)


            # Creation de l'objet twist Command
            command = Base_pb2.TwistCommand()

            # Initialisation de l'objet 
            command.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_TOOL
            command.duration = duration #0
        
            twist = command.twist
            twist.linear_x = twistValues.linear_x 
            twist.linear_y = twistValues.linear_y
            twist.linear_z = twistValues.linear_z 
            twist.angular_x = twistValues.angular_x 
            twist.angular_y = twistValues.angular_y 
            twist.angular_z = twistValues.angular_z 

             # print ("Sending the twist command for ", duration , " seconds...")
            print ("Twist Command sent to the robot ")
            self.base_client.SendTwistCommand(command)
            print ("Twist Command sent to the robot - done ")


            e = threading.Event()
            notification_handle = self.base_client.OnNotificationControllerTopic(
                self.check_for_end_or_abort_Twist(e),
                Base_pb2.NotificationOptions()
            )

            #notification_handle = self.base_client.OnNotificationActionTopic(
            ##    self.check_for_end_or_abort_Twist(e),
            #    Base_pb2.NotificationOptions()
            #)             
            
            #print ("Waiting... ")
            #finished = e.wait(duration+2)
            #self.base_client.Unsubscribe(notification_handle)

            # Let time for twist to be executed
            #if (finished) :
            #   print ("Twinst Commande Finished ")
            #else :
            #    print ("Twinst Commande NOT Finished ")
            #    time.sleep(duration) 

            time.sleep(duration) 

            print ("Stopping the robot...")
            self.base_client.Stop()

            return True
        else : 
            if (TRACE == True) : 
                print ("[WARN]" , NOT_CONNECTED_MSG)
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
                 print ("[WARN]" , NOT_CONNECTED_MSG)

            return False
        
        # Client connected to the robot 
        if (TRACE == True) : 
                print ("[Info]" , JOINT_SPEED_CMD_MSG)


        joint_speeds = Base_pb2.JointSpeeds()
        actuator_count = self.base_client.GetActuatorCount().count

        # The 7DOF robot will spin in the same direction for 10 seconds
        # print ("Number of actuators : " , actuator_count)
        if actuator_count == 7:
            # speeds = [SPEED, 0, -SPEED, 0, SPEED, 0, -SPEED]
            i = 0
        speeds = jointSpeedValues.speedJointList() 
        
        for speed in speeds:
            print ("Actuator " , i , " - Speed : " , speed )
            joint_speed = joint_speeds.joint_speeds.add()
            joint_speed.joint_identifier = i 
            joint_speed.value = speed
            joint_speed.duration = 0
            i = i + 1
        
        # print ("Sending the joint speeds for 10 seconds...")
        self.base_client.SendJointSpeedsCommand(joint_speeds)
        time.sleep(duration) # 10seconds 

        #print ("Stopping the robot")
        self.base_client.Stop()

        return True

    ##
    #
    ##
    def perform(self , user_action) : 
        # TODO : CHECK if CONNECTED 
        
        action_type = user_action.action_type()

        if (action_type == HOME_POSITION ) : 
            self.move_to_Home_position()             
        
        elif (action_type == PREDEF_POSITION ) : 
            self.move_to_predefined_position(user_action.get_position_label() ) 
            
        elif (action_type ==CARTESIAN_POSITION) : 
            self.move_to_cartesian(user_action.get_cartesian_position())
            
        elif (action_type ==POSITION_ANGLES ) : 
            pass
        elif     (action_type ==JOINT_TWIST ) :
            self.twist_command(user_action.get_twist_values() , user_action.get_duration())
            pass
        elif (action_type ==JOINT_SPEED) :  
            pass 
        else : 

            print("Problem")

        
    ## ----------------------------------------------------------------------------
    # Plays a sequence of tasks defined in _action_sequence object 
    #
    ## ----------------------------------------------------------------------------
    def play_sequence(self , _action_sequence) : 

        e = threading.Event()
        notification_handle = self.base_client.OnNotificationSequenceInfoTopic(
            self.check_for_sequence_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )
        print("Creating sequence on device and executing it")
        handle_sequence = self.base_client.CreateSequence(_action_sequence.get_sequence())
        self.base_client.PlaySequence(handle_sequence)
        
        print("Waiting for movement to finish ...")
        finished = e.wait(TIMEOUT_DURATION)

        self.base_client.Unsubscribe(notification_handle)


        if not finished:
            print("Timeout on action notification wait")

        return finished






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
    