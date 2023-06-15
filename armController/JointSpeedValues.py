##
#  Data type holding the 7 Joint speed values - one for each DOF 
#
##

class JointSpeedValues :

    def __init__(self, speedValuesList=[0.0 , 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) : 
        self.jointSpeedValuesList = speedValuesList 
        

    ##
    #
    ##
    def get_speedValues(self) :
        return self.jointSpeedValuesList

    ##
    #
    ##
    def display(self) :
        print ("Joint Speed Values : ")
        print ("   " , self.jointSpeedValuesList) 
