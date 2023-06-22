##  ---------------------------------------------------------------------
#  Data type holding the 7 Joint speed values - one for each  JOINT
#
##
class JointSpeedValues :

    # ---------------------------------------------------------------------
    # Constructor 
    # Set 7 attributes corresponding to the joint speed (one to seven)
    # ---------------------------------------------------------------------
    def __init__(self , _speedJoint1 , _speedJoint2, _speedJoint3, _speedJoint4 ,\
                        _speedJoint5 , _speedJoint6 , _speedJoint7) : 
        self.speedJoint1 = _speedJoint1 
        self.speedJoint2 = _speedJoint2
        self.speedJoint3 = _speedJoint3
        self.speedJoint4 = _speedJoint4
        self.speedJoint5 = _speedJoint5
        self.speedJoint6 = _speedJoint6
        self.speedJoint7 = _speedJoint7



    ## ---------------------------------------------------------------------
    # Retruns the speed joint attributes as a list 
    ## ---------------------------------------------------------------------
    def speedJointList(self) : 
        res = []
        res.append(self.speedJoint1)
        res.append(self.speedJoint2)
        res.append(self.speedJoint3)
        res.append(self.speedJoint4)
        res.append(self.speedJoint5)
        res.append(self.speedJoint6)
        res.append(self.speedJoint7)

        return res

   
    ## ---------------------------------------------------------------------
    # Display the joint speed values 
    ## ---------------------------------------------------------------------
    def display(self) :
        print ("Joint Speed Values : ")
        print ("   " , self.jointSpeed1 ,", " ,  self.jointSpeed2 ,", ", self.jointSpeed3, ", ", self.jointSpeed4 ,", ",\
              self.jointSpeed5 ,", " , self.jointSpeed6 ,", ", self.jointSpeed7 ) 
