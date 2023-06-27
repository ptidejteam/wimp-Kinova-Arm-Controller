
# Global Variables : 
IP_ADRESSE = "192.168.0.10"   # IP Adresse of the ARM
USERNAME = "admin"            # username and password : used to create a session
PWD = "admin"
TCP_PORT = 10000              # TCP Port : used for high level control 
UDP_PORT = 10001              # UDP Port : used for low  level control 
TRACE = True                  # Boolean enabling/desabling trace printing 
SESSION_INACTIVITY_TIMEOUT    = 60000 # (milliseconds)
CONNECTION_INACTIVITY_TIMEOUT = 2000  # (milliseconds)

 
TIMEOUT_DURATION = 20

## 


## 
# Constants corresponding to messages that will be displayed to the user 
#
##
NOT_CONNECTED_MSG = "Not connected to the robot"
DISCONNECT_MSG    = "Disconnexion completed" 
CARTESIAN_MV_ACTION_MSG = "Movement to cartesian position"
READ_CART_VALUES_MSG = "Reading cartesian position Values"
TWIST_CMD_MSG = "Sending Twist command"
JOINT_SPEED_CMD_MSG = "Sending a joint speed command"
MOVE_TO_POSITION_ANGLES_MSG = "Movement to a position defined by the given angles"
MOVE_TO_PREDEFINED_POSITION_MSG = "Moving to a predefined position"

##
#
##
def msg_print(ttype , message) : 
    print("[" , ttype , "] " , message) ; 