##
#  Holds a cartesian Values : 
#   pos_x, pos_y and pos_z according to the 3 axes 
#   theta_x, theta_y and theta_z : the three angles of the arm 
#   relatively to the three axes 
#
#  Note that, one or many attributes could be None value
# 
#
##

class CartesianPosition :

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self) : 
        self.pos_x = None
        self.pos_y = None 
        self.pos_z = None 
        self.theta_x = None 
        self.theta_y = None 
        self.theta_z = None 
        
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, x , y , z, ang_x=None , ang_y=None, ang_z=None) : 
        self.pos_x = x
        self.pos_y = y  
        self.pos_z = z 
        self.theta_x = ang_x
        self.theta_y = ang_y
        self.theta_z = ang_z 

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set_position_values(self, x , y , z ) :
        self.pos_x = x
        self.pos_y = y  
        self.pos_z = z 
        self.theta_x = None
        self.theta_y = None
        self.theta_z = None 

        pass

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set_angles_values(self, ang_x , ang_y , ang_z ) :
        self.pos_x = None
        self.pos_y = None  
        self.pos_z = None 
        self.theta_x = ang_x
        self.theta_y = ang_y
        self.theta_z = ang_z 

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set_values(self, x , y , z, ang_x , ang_y , ang_z) : 
        self.pos_x = x
        self.pos_y = y  
        self.pos_z = z 
        self.theta_x = ang_x
        self.theta_y = ang_y
        self.theta_z = ang_z 

    ## -----------------------------------------------------------------------
    #
    #
    ## -----------------------------------------------------------------------
    def display(self) : 
        print(" Cartesian Values : ")
        print ("    (Coord. - X,Y,Z): " , self.pos_x , ", " , self.pos_y , ", " , self.pos_z)
        print ("    (Angles - X,Y,Z): " , self.theta_x , ", " , self.theta_y, ", " , self.theta_z  )