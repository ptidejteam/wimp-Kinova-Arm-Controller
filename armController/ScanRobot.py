##
# JE DOIS faire la revue du code 
#
##

from kortex_api.autogen.client_stubs.DeviceManagerClientRpc import DeviceManagerClient 
from kortex_api.autogen.client_stubs.DeviceConfigClientRpc import DeviceConfigClient 
from kortex_api.RouterClient import RouterClient, RouterClientSendOptions
from kortex_api.autogen.messages import Common_pb2

from google.protobuf import json_format

from armController.ArmController import ArmController, TRACE
from armController.ConstantsUtilities import NOT_CONNECTED_MSG

##
#
#
##
class ScanRobot :

    def __init__(self , _armController):
        self.armController  = _armController
        


    ##
    #  Scan the devices of the ARM. Displays : 
    #    - Device type
    #    - Firmware Version
    #    - MAC Adress 
    #    - Etc. 
    #
    ##
    def scan_devices(self):
         # Api initialisation
         if (self.armController.isConnected() == True) : 
             
             router = self.armController.get_router() 

             device_manager = DeviceManagerClient(router)
             device_config = DeviceConfigClient(router)


             # Get all device routing information (from DeviceManagerClient service)
             all_devices_info = device_manager.ReadAllDevices()

             options = RouterClientSendOptions()
             options.timeout_ms = 4000

             # Use device routing information to route to every devices (base, actuator, interconnect, etc.) in the arm/base system and request their general device information
             for dev in all_devices_info.device_handle:
                 device_info = {}
                 device_info.update( json_format.MessageToDict( device_config.GetDeviceType           (dev.device_identifier, options) ) )
                 device_info.update( json_format.MessageToDict( device_config.GetFirmwareVersion      (dev.device_identifier, options) ) )
                 device_info.update( json_format.MessageToDict( device_config.GetBootloaderVersion    (dev.device_identifier, options) ) )
                 device_info.update( json_format.MessageToDict( device_config.GetModelNumber          (dev.device_identifier, options) ) )
                 device_info.update( json_format.MessageToDict( device_config.GetPartNumber           (dev.device_identifier, options) ) )
                 device_info.update( json_format.MessageToDict( device_config.GetPartNumberRevision   (dev.device_identifier, options) ) )
                 device_info.update( json_format.MessageToDict( device_config.GetSerialNumber         (dev.device_identifier, options) ) )

             # Get hexadecimal representation of MAC address
             macAddress_hexstr = ""
             for b in device_config.GetMACAddress(dev.device_identifier, options).mac_address:
                 macAddress_hexstr += "%02X:" % b
             macAddress_hexstr = macAddress_hexstr[:-1] # remove last ':'
             device_info.update( { "macAddress": macAddress_hexstr } )
             print("-----------------------------")

             print("-- {}: id = {} --".format(Common_pb2._DEVICETYPES.values_by_number[dev.device_type].name, dev.device_identifier))
             for key, value in device_info.items():
                 print(str("%20s") % key + ": " + str(value))


         else : 
             if (TRACE == True) : 
                 print ("[WARN]" , NOT_CONNECTED)