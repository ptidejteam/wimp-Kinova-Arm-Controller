##
#
# Implements a low level command to the gripper 
# Code based on Kinova Examples 
#
# @modified by El hachemi Alikacem
# @date 15 june 2023
#
## -----------------------------------------------------------------------

from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from kortex_api.autogen.messages import Base_pb2
from kortex_api.autogen.messages import BaseCyclic_pb2
from kortex_api.autogen.client_stubs.GripperCyclicClientRpc import GripperCyclicClient

from kortex_api.UDPTransport import UDPTransport
from kortex_api.RouterClient import RouterClient, RouterClientSendOptions
from kortex_api.autogen.messages import Session_pb2
from kortex_api.SessionManager import SessionManager


from armController.ConstantsUtilities import IP_ADRESSE , UDP_PORT, USERNAME , PWD, \
    SESSION_INACTIVITY_TIMEOUT, CONNECTION_INACTIVITY_TIMEOUT

import time 

errorLLCallback = lambda kException: print("_______ low level callback error _________ {}".format(kException))


class GripperLowlevelControl : 
        
    def __init__(self, _armController , proportional_gain = 2.0):
        """
           In the first section, creation of :
                - Transport Object (UDPTransport)
                - Session (SessionManager)
        """

        # TODO : Check if connected to the client 

        self.armController = _armController 
        self.UDP_Transport = UDPTransport() 
        self.router_real_time = RouterClient(self.UDP_Transport , errorLLCallback )
        self.UDP_Transport.connect(IP_ADRESSE, UDP_PORT)

        # Create a Session
        session_info = Session_pb2.CreateSessionInfo()
        session_info.username = USERNAME
        session_info.password = PWD
        session_info.session_inactivity_timeout = SESSION_INACTIVITY_TIMEOUT  
        session_info.connection_inactivity_timeout = CONNECTION_INACTIVITY_TIMEOUT

        self.UDP_session_manager = SessionManager(self.router_real_time)
        self.UDP_session_manager.CreateSession(session_info)


        """
            GripperLowLevelExample class constructor.

            Inputs:
                kortex_api.RouterClient router:            TCP router
                kortex_api.RouterClient router_real_time:  Real-time UDP router
                float proportional_gain: Proportional gain used in control loop (default value is 2.0)

            Outputs:
                None
            Notes:
                - Actuators and gripper initial position are retrieved to set initial positions
                - Actuator and gripper cyclic command objects are created in constructor. Their
                  references are used to update position and speed.
        """

        self.proportional_gain = proportional_gain

        ###########################################################################################
        # UDP and TCP sessions are used in this example.
        # TCP is used to perform the change of servoing mode
        # UDP is used for cyclic commands.
        #
        # 2 sessions have to be created: 1 for TCP and 1 for UDP
        ###########################################################################################

        # RM 
        #self.router = _router
        # DONE
        #self.router_real_time = _udpRouter 


        # Create base client using TCP router
        # 
        #self.base = _base  USE : armController.base_clien

        # Create base cyclic client using UDP router.
        self.base_cyclic = BaseCyclicClient(self.router_real_time)

        # Create base cyclic command object.
        self.base_command = BaseCyclic_pb2.Command()
        self.base_command.frame_id = 0
        self.base_command.interconnect.command_id.identifier = 0
        self.base_command.interconnect.gripper_command.command_id.identifier = 0

        # Add motor command to interconnect's cyclic
        self.motorcmd = self.base_command.interconnect.gripper_command.motor_cmd.add()

        # Set gripper's initial position velocity and force
        base_feedback = self.base_cyclic.RefreshFeedback()
        self.motorcmd.position = base_feedback.interconnect.gripper_feedback.motor[0].position
        self.motorcmd.velocity = 0
        self.motorcmd.force = 100 
        
        for actuator in base_feedback.actuators:
            self.actuator_command = self.base_command.actuators.add()
            self.actuator_command.position = actuator.position
            self.actuator_command.velocity = 0.0
            self.actuator_command.torque_joint = 0.0
            self.actuator_command.command_id = 0
            print("Position = ", actuator.position)
        
        # Save servoing mode before changing it
        self.previous_servoing_mode = self.armController.base_client.GetServoingMode()

        # Set base in low level servoing mode
        servoing_mode_info = Base_pb2.ServoingModeInformation()
        servoing_mode_info.servoing_mode = Base_pb2.LOW_LEVEL_SERVOING
        self.armController.base_client.SetServoingMode(servoing_mode_info)

        self.gripper_cyclic = GripperCyclicClient(self.armController.get_router()) 

    
    ## TO REMOVE 
    def feedback(self) :        
        feedback = self.gripper_cyclic.RefreshFeedback() 
        
    
    #
    def terminate(self) : 
        """
            Restore arm's servoing mode to the one that
            was effective before running the example.

            Inputs:
                None
            Outputs:
                None
            Notes:
                None

        """
        # Restore servoing mode to the one that was in use before running the example
        self.armController.base_client.SetServoingMode(self.previous_servoing_mode) 


    ## ------------------------------------------------------------------------------
    # 
    ## ------------------------------------------------------------------------------
    def reachGripperPosition(self , target_position) :
            
        """
            Position gripper to a requested target position using a simple
            proportional feedback loop which changes speed according to error
            between target position and current gripper position

            Inputs:
                float target_position: position (0% - 100%) to send gripper to.
            Outputs:
                Returns True if gripper was positionned successfully, returns False
                otherwise.
            Notes:
                - This function blocks until position is reached.
                - If target position exceeds 100.0, its value is changed to 100.0.
                - If target position is below 0.0, its value is set to 0.0.
        """
        if target_position > 100.0:
            target_position = 100.0
        if target_position < 0.0:
            target_position = 0.0
        
        while True:
            try:
                base_feedback = self.base_cyclic.Refresh(self.base_command)

                # Calculate speed according to position error (target position VS current position)
                position_error = target_position - base_feedback.interconnect.gripper_feedback.motor[0].position

                # If positional error is small, stop gripper
                if abs(position_error) < 1.5:
                    position_error = 0
                    self.motorcmd.velocity = 0
                    self.base_cyclic.Refresh(self.base_command)
                    return True
                else:
                    self.motorcmd.velocity = self.proportional_gain * abs(position_error) # Velocity decreases 
                    
                    if self.motorcmd.velocity > 100.0:
                        self.motorcmd.velocity = 100.0
                    self.motorcmd.position = target_position
                    #print ("V=" , self.motorcmd.velocity , "F=" , self.motorcmd.force )
            except Exception as e:
                print("Error in refresh: " + str(e))
                return False
            time.sleep(0.001)
        return True

         
