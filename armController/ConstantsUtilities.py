
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
NOT_CONNECTED = "Not connected to the robot"
DISCONNECT    = "Disconnexion completed" 
CARTESIAN_MV_ACTION = "Movement to cartesian position"
READ_CART_VALUES = "Reading cartesian position Values"
TWIST_CMD = "Sending Twist command"
JOINT_SPEED_CMD = "Sending a joint speed command"
MOVE_TO_POSITION_ANGLES = "Movement to a position defined by the given angles"


##
#
##
def msg_print(ttype , message) : 
    print("[" , ttype , "] " , message) ; 