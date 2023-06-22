##
# Data type to hold the angles for the 7 joints 
# Angles are in degree and could be negative 
#
##

class JointAnglesValues :
    
    ## ------------------------------------------------------------
    #
    ## ------------------------------------------------------------
    def __init__(self , _angleJoint1 , _angleJoint2, _angleJoint3, _angleJoint4 ,\
                        _angleJoint5 , _angleJoint6 , _angleJoint7) : 
        self.angleJoint1 = _angleJoint1 
        self.angleJoint2 = _angleJoint2
        self.angleJoint3 = _angleJoint3
        self.angleJoint4 = _angleJoint4
        self.angleJoint5 = _angleJoint5
        self.angleJoint6 = _angleJoint6
        self.angleJoint7 = _angleJoint7

    ## ------------------------------------------------------------
    #
    ## ------------------------------------------------------------
    def angleJointList(self) : 
        res = []
        res.append(self.angleJoint1)
        res.append(self.angleJoint2)
        res.append(self.angleJoint3)
        res.append(self.angleJoint4)
        res.append(self.angleJoint5)
        res.append(self.angleJoint6)
        res.append(self.angleJoint7)

        return res
