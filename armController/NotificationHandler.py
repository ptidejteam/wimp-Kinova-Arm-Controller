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


##
#
##
class NotificationHandler : 
    def __init__(self , _base_client) :
        if (_base_client != None) : 
            self.base_client = _base_client 
            self.handler_list = []
        else :
            #TODO : Display a Message : Can't process notifications 
            pass
            
    ##
    #
    ##
    def subscribe(self) :       
        def configChangeNotification_callback(data):
            print("*****************************************************")
            print("* Notification callback for :  Configuration Change *")
            print(json_format.MessageToJson(data))
            print("*****************************************************")

        def controlModeNotification_callback(data):
            print("*********************************************")
            print("*  Notification callback for : Control Mode *")
            print(json_format.MessageToJson(data))
            print("*********************************************")

        def armStatNotification_callback(data):
            print("*********************************************")
            print("*  Notification callback for : Arm State    *")
            print(json_format.MessageToJson(data))
            print("*********************************************")

        def actionNotification_callback(data):
            print("*********************************************")
            print("*  Notification callback for : Action       *")
            print(json_format.MessageToJson(data))
            print("*********************************************")

        def controllerNotification_callback(data):
            print("*********************************************")
            print("*  Notification callback for : Controller   *")
            print(json_format.MessageToJson(data))
            print("*********************************************")


        # Il y a 14 methodes correspondant à l'enregistrement aux notifications 
        #
        #base_client1 =  BaseClient(self.router) TO REMOVE 
        #base_client1.OnNo

        notif_handle = self.base_client.OnNotificationArmStateTopic(armStatNotification_callback ,Base_pb2.NotificationOptions())
        self.handler_list.append(notif_handle)

        #self.base_client.OnNotification
        
        
        # Notification for Configuration Change : 
        #notif_handle = self.base_client.OnNotificationConfigurationChangeTopic(configChangeNotification_callback,Base_pb2.NotificationOptions())
        #self.handler_list.append(notif_handle)


        # Notification for Control Mode : probably When it changes from Low level to high level and vice versa 
        notif_handle = self.base_client.OnNotificationControlModeTopic(controlModeNotification_callback,Base_pb2.NotificationOptions())
        self.handler_list.append(notif_handle)


        # Notification for an Action (tested) 
        notif_handle = self.base_client.OnNotificationActionTopic(actionNotification_callback,Base_pb2.NotificationOptions())
        self.handler_list.append(notif_handle)

        ##
        notif_handle = self.base_client.OnNotificationControllerTopic(controllerNotification_callback,Base_pb2.NotificationOptions()) 
        self.handler_list.append(notif_handle)

        #ActionTopic(actionNotification_callback,Base_pb2.NotificationOptions())
        #self.handler_list.append(notif_handle)

        

        # Notification for Mapping Info Change : No Idea 
        # notif_handle = self.base_client.OnNotificationMappingInfoTopic() 
        #self.handler_list.append(notif_handle)

        # Notification for 
        #notif_handle = self.base_client.OnNotificationOperatingModeTopic()
        #self.handler_list.append(notif_handle)

        # Notification for 
        #notif_handle = self.base_client.OnNotificationSequenceInfoTopic() 
        #self.handler_list.append(notif_handle)

        # Notification for 
        #notif_handle = self.base_client.OnNotificationProtectionZoneTopic()
        #self.handler_list.append(notif_handle)

        # Notification for 
        #notif_handle = self.base_client.OnNotificationUserTopic
        #self.handler_list.append(notif_handle)

        
    ##
    #
    ##
    def unsubscribe(self) :
        if (self.handler_list != None) : 
            for one_handler in self.handler_list :                
                self.base_client.Unsubscribe(one_handler)  

