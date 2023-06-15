##
#  Holds a Twist Values : 
#   linear_x,  linear_x and linear_x : speed according to the corresponding axe (metre / second, 
#   Example : 0.03 means 3 cm per second 
#
#   angular_x, angular_y, angular_z, speed (degree per second). Exemple : 5.0 means 5degrees per second 
#
#
##

class TwistValues :

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self) : 
        self.linear_x = 0.0  # 
        self.linear_y = 0.0  # 
        self.linear_z = 0.0  # 
        self.angular_x = 0.0 # 
        self.angular_y = 0.0 # 
        self.angular_z = 0.0 # 
        
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, lin_x , lin_y , lin_z, ang_x=0.0 , ang_y=0.0 , ang_z=0.0 ) : 
        self.linear_x = lin_x   # 
        self.linear_y = lin_y   # 
        self.linear_z = lin_z   # 
        self.angular_x = ang_x  # 
        self.angular_y = ang_y  # 
        self.angular_z = ang_z  # 

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set_linear_values(self, lin_x , lin_y , lin_z )  :
        self.linear_x = lin_x 
        self.linear_y = lin_y   
        self.linear_z = lin_z   
        self.angular_x = 0.0    
        self.angular_y = 0.0    
        self.angular_z = 0.0   


    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set_angular_values(self, ang_x , ang_y , ang_z) : 
        self.linear_x = 0.0
        self.linear_y = 0.0
        self.linear_z = 0.0
        self.angular_x = ang_x  
        self.angular_y = ang_y   
        self.angular_z = ang_z 

    ## -----------------------------------------------------------------------
    #
    #
    ## -----------------------------------------------------------------------
    def display(self) : 
        print(" Twist Values : ")
        print ("    (Linear - X,Y,Z): " , self.linear_x , ", " , self.linear_y , ", " , self.linear_z )
        print ("    (Angles - X,Y,Z): " , self.angular_x , ", " , self.angular_y, ", " , self.angular_z )