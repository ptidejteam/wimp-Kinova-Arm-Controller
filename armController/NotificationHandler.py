##
# Implements Notification handling 
# 
#
# @auteur el hachemi alikacem
# @date 18 june 2023
##
from kortex_api.autogen.messages import Base_pb2
from google.protobuf import json_format


from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient

ACTION_NOTIF         = 0
ARM_STATE_NOTIF      = 1 
CONFIG_CHANGE_NOTIF  = 2 
# CONTROL_MODE_NOTIF   = 3 # corresponding Notification handler fonction is deprecated 
CONTROLLER_NOTIF     = 4
FACTORY_NOTIF        = 5
MAPPING_INFO_NOTIF   = 6
NETWORK_NOTIF        = 7
OPER_MODE_NOTIF      = 8
PROTECT_ZONE_NOTIF   = 9
ROBOT_EVENT_NOTIF    = 10
SEQ_INFO_NOTIF       = 11
SERV_MODE_NOTIF      = 12
USER_NOTIF_NOTIF     = 13

"""
base_client2.OnNotificationActionTopic
base_client2.OnNotificationArmStateTopic
base_client2.OnNotificationConfigurationChangeTopic
base_client2.OnNotificationControlModeTopic
base_client2.OnNotificationControllerTopic
base_client2.OnNotificationFactoryTopic
base_client2.OnNotificationMappingInfoTopic
base_client2.OnNotificationNetworkTopic
base_client2.OnNotificationOperatingModeTopic
base_client2.OnNotificationProtectionZoneTopic
base_client2.OnNotificationRobotEventTopic
base_client2.OnNotificationSequenceInfoTopic
base_client2.OnNotificationServoingModeTopic
base_client2.OnNotificationUserTopic
"""


def configChangeNotification_callback(data):
        print("*****************************************************")
        print("* Notification callback for :  Configuration Change *")
        print(json_format.MessageToJson(data))
        print("*****************************************************")

    ## -------------------------------------------------------------------------
    ## -------------------------------------------------------------------------
def controlModeNotification_callback(data):
        print("*********************************************")
        print("*  Notification callback for : Control Mode *")
        print(json_format.MessageToJson(data))
        print("*********************************************")

    ## -------------------------------------------------------------------------
    ## -------------------------------------------------------------------------
def armStatNotification_callback(data):
        print("*********************************************")
        print("*  Notification callback for : Arm State    *")
        print(json_format.MessageToJson(data))
        print("*********************************************")

    ## -------------------------------------------------------------------------
    ## -------------------------------------------------------------------------
def actionNotification_callback(data):
        print("*********************************************")
        print("*  Notification callback for : Action       *")
        print(json_format.MessageToJson(data))
        print("*********************************************")

 ## -------------------------------------------------------------------------
 ## -------------------------------------------------------------------------
def controllerNotification_callback(data):
        print("*********************************************")
        print("*  Notification callback for : Controller   *")
        print(json_format.MessageToJson(data))
        print("*********************************************")



## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def factoryNotification_callback(data):
    print("*********************************************")
    print("*  Notification callback for : Factory      *")
    print(json_format.MessageToJson(data))
    print("*********************************************")

## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def mappingInfoNotification_callback(data) :
    print("*********************************************")
    print("*  Notification callback for : Mapping Info *")
    print(json_format.MessageToJson(data))
    print("*********************************************")


## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def networkNotification_callback(data) :
    print("*********************************************")
    print("*  Notification callback for : Network      *")
    print(json_format.MessageToJson(data))
    print("*********************************************")


## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def operatingNotification_callback(data):
    print("*********************************************")
    print("* Notification callback for : Operating Mode*")
    print(json_format.MessageToJson(data))
    print("*********************************************")


## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def protectionZoneNotification_callback(data):
    print("***********************************************")
    print("* Notification callback for : Protection Zone *")
    print(json_format.MessageToJson(data))
    print("***********************************************")

## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def robotEventNotification_callback(data):
    print("*********************************************")
    print("*  Notification callback for : Robot Event  *")
    print(json_format.MessageToJson(data))
    print("*********************************************")


## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def sequenceInfoNotification_callback(data) :
    print("*********************************************")
    print("* Notification callback for : Sequence Info *")
    print(json_format.MessageToJson(data))
    print("*********************************************")


## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def servoingModeNotification_callback(data) :
    print("*********************************************")
    print("* Notification callback for : Servoing Mode *")
    print(json_format.MessageToJson(data))

## -------------------------------------------------------------------------
## -------------------------------------------------------------------------
def userNotification_callback(data):
    print("*********************************************")
    print("*  Notification callback for : User         *")
    print(json_format.MessageToJson(data))




## -------------------------------------------------------------------------
##
#
## -------------------------------------------------------------------------
class NotificationHandler : 
    ## -------------------------------------------------------------------------
    #
    ## -------------------------------------------------------------------------
    def __init__(self , _base_client) :
        if (_base_client != None) : 
            self.base_client = _base_client 
            self.handler_list = [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        else :
            #TODO : Display a Message : Can't process notifications 
            pass
            
 
    ## -------------------------------------------------------------------------
    ## Subsribe to all the defined notifications 
    ## -------------------------------------------------------------------------
    def subscribeAll(self) :   
        self.subscribe(ACTION_NOTIF)
        self.subscribe(ARM_STATE_NOTIF)
        self.subscribe(CONFIG_CHANGE_NOTIF) 
        # self.subscribe(CONTROL_MODE_NOTIF)  - DEPRECATED 
        self.subscribe(CONTROLLER_NOTIF)
        self.subscribe(FACTORY_NOTIF)
        self.subscribe(MAPPING_INFO_NOTIF)
        self.subscribe(NETWORK_NOTIF)
        self.subscribe(OPER_MODE_NOTIF)
        self.subscribe(PROTECT_ZONE_NOTIF)
        self.subscribe(ROBOT_EVENT_NOTIF)
        self.subscribe(SEQ_INFO_NOTIF)
        self.subscribe(SERV_MODE_NOTIF)
        self.subscribe(USER_NOTIF_NOTIF)
                
    ## -------------------------------------------------------------------------
    ## -------------------------------------------------------------------------
    def subscribe(self , notification_type) :       
      
        # Il y a 14 methodes correspondant à l'enregistrement aux notifications 
        #
        
        if notification_type == ACTION_NOTIF : #0
            # Notification for an Action (tested) 
            notif_handle = self.base_client.OnNotificationActionTopic(actionNotification_callback,Base_pb2.NotificationOptions())
            self.handler_list[ACTION_NOTIF] = notif_handle
            
        elif notification_type == ARM_STATE_NOTIF : #1
            notif_handle = self.base_client.OnNotificationArmStateTopic(armStatNotification_callback ,Base_pb2.NotificationOptions())
            self.handler_list[ARM_STATE_NOTIF] = notif_handle
            
        elif notification_type == CONFIG_CHANGE_NOTIF  : #2
            notif_handle = self.base_client.OnNotificationConfigurationChangeTopic(configChangeNotification_callback,Base_pb2.NotificationOptions())
            self.handler_list[CONFIG_CHANGE_NOTIF] = notif_handle
        # The next notification handler (OnNotificationControlModeTopic) is DEPRECATED, It's better to not use 
        #elif notification_type == CONTROL_MODE_NOTIF   : #3
            # Notification for Control Mode : probably When it changes from Low level to high level and vice versa 
        #    notif_handle = self.base_client.OnNotificationControlModeTopic(controlModeNotification_callback,Base_pb2.NotificationOptions())
        #    self.handler_list[CONTROL_MODE_NOTIF] = notif_handle
        
        elif notification_type == CONTROLLER_NOTIF     : #4
            notif_handle = self.base_client.OnNotificationControllerTopic(controllerNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[CONTROLLER_NOTIF]= notif_handle

        elif notification_type == FACTORY_NOTIF        : #5
            notif_handle = self.base_client.OnNotificationFactoryTopic (factoryNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[FACTORY_NOTIF]= notif_handle

        elif notification_type == MAPPING_INFO_NOTIF   : #6
            notif_handle = self.base_client.OnNotificationMappingInfoTopic (mappingInfoNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[MAPPING_INFO_NOTIF]= notif_handle            
            
        elif notification_type == NETWORK_NOTIF        : #7
            notif_handle = self.base_client.OnNotificationNetworkTopic(networkNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[NETWORK_NOTIF]= notif_handle            
           

        elif notification_type == OPER_MODE_NOTIF      : #8
            notif_handle = self.base_client.OnNotificationOperatingModeTopic(operatingNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[OPER_MODE_NOTIF]= notif_handle            
            
        elif notification_type == PROTECT_ZONE_NOTIF   : #9
            notif_handle = self.base_client.OnNotificationProtectionZoneTopic(protectionZoneNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[PROTECT_ZONE_NOTIF]= notif_handle            
  
        elif notification_type == ROBOT_EVENT_NOTIF    : #10
            notif_handle = self.base_client.OnNotificationProtectionZoneTopic(robotEventNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[ROBOT_EVENT_NOTIF]= notif_handle            

        elif notification_type == SEQ_INFO_NOTIF       : #11
            notif_handle = self.base_client.OnNotificationSequenceInfoTopic(sequenceInfoNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[SEQ_INFO_NOTIF]= notif_handle            

        elif notification_type == SERV_MODE_NOTIF      : #12
            notif_handle = self.base_client.OnNotificationServoingModeTopic(servoingModeNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[SERV_MODE_NOTIF]= notif_handle            

        elif notification_type == USER_NOTIF_NOTIF     : #= 13
            notif_handle = self.base_client.OnNotificationUserTopic(userNotification_callback,Base_pb2.NotificationOptions()) 
            self.handler_list[USER_NOTIF_NOTIF]= notif_handle            

        else : 
            print ("Not expected ")

       

       
        ##

        #ActionTopic(actionNotification_callback,Base_pb2.NotificationOptions())
        #self.handler_list.append(notif_handle)

        

        # Notification for Mapping Info Change : No Idea 
       

        

    ## -------------------------------------------------------------------------
    #
    ## -------------------------------------------------------------------------
    def unsubscribe(self) :        
        if (self.handler_list != None) : 
            for one_handler in self.handler_list :                
                if one_handler != None :
                    self.base_client.Unsubscribe(one_handler)  
