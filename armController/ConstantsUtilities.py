
NOT_CONNECTED = "Not connected to the robot"
DISCONNECT    = "Disconnexion completed" 
CARTESIAN_MV_ACTION = "Movement to cartesian position"
READ_CART_VALUES = "Reading cartesian position Values"
TWIST_CMD = "Sending Twist command"
JOINT_SPEED_CMD = "Sending a joint speed command"
MOVE_TO_POSITION_ANGLES = "Movement to a position defined by the given angles"

def msg_print(ttype , message) : 
    print("[" , ttype , "] " , message) ; 