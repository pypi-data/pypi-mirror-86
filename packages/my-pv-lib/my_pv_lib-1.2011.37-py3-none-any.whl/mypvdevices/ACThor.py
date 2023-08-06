#!/usr/bin/python

from _pytest.compat import STRING_TYPES
from colr import color
from datetime import datetime, timedelta
import logging
import time
import threading
import json
from pyModbusTCP.client import ModbusClient

from ModbusTcpDevice import ModbusTcpDevice
# from mypvdevices.ModbusConnection import ModbusConnection

BUILDNR = "4321"

class ACThor(ModbusTcpDevice):
    __deviceType__ = "AC Thor"

    def __init__(self, serial):
        ModbusTcpDevice.__init__(self, serial)

    # def getIdentifier(self):
    #     return self.getSerial() + ", Node: " + str(self.__nodeId__)
    
    # def __supervise__(self):
        
    #     value = self.getDataset("temp1")
    #     if value != None and ( value > 1200 or value < 0 ):
    #         logging.error("[Device] " + self.getIdentifier() + " - Temp1 sensor error: " + str(value))
    #         temp1error = True
    #     else:
    #         temp1error = False

    #     value = self.getDataset("temp2")
    #     if value != None and ( value > 1200 or value < 0 ):
    #         logging.error("[Device] " + self.getIdentifier() + " - Temp2 sensor error: " + str(value))
    #         temp2error = True
    #     else:
    #         temp2error = False

    #     value = self.getDataset("tempchip")
    #     if value == 0 :
    #         logging.error("[Device] " + self.getIdentifier() + " - No IR Connection to Device.")
    #         irError = True
    #     else:
    #         irError = False

    #     value = self.getDataset("operation_mode")
    #     if value != None and value > 100 :
    #         logging.error("[Device] " + self.getIdentifier() + " - Operation Mode " + str(value) + " detected.")
    #         opmodeError = True
    #     else:
    #         opmodeError = False

    #     modbusErrorRate = self.getCommunicationErrorsRate()
    #     if modbusErrorRate != None and modbusErrorRate > MODBUSWARNLEVEL and modbusErrorRate < 1:
    #         logging.error("[Device] " + self.getIdentifier() + " - Modbus error rate to hight " + str(modbusErrorRate) + ".")
    #         modbusWarning = True
    #     else:
    #         modbusWarning = False
    #     if modbusErrorRate == 1 :
    #         logging.error("[Device] " + self.getIdentifier() + " - Modbus communication to device not working.")
    #         modbusError = True
    #     else:
    #         modbusError = False

    #     if self.__checkRegiterTimeStamp__() != True:
    #         logging.error("[Device] " + self.getIdentifier() + " - Register values to old. Communication errors expected.")
    #         registerError = True
    #     else:
    #         registerError = False

    #     healthState = 0

    #     #healthState warnings
    #     if temp2error == True or irError == True or opmodeError == True or modbusWarning == True:
    #         healthState = 1

    #     #healthState errors
    #     if temp1error == True or modbusError == True or registerError == True:
    #         healthState = 2

    #     self.__setHealthState__(healthState)

    def __getRegisterMapping__(self):
        datasets = {}
        datasets["day_counter"] = self.__createDataset__(1000, "avg")
        datasets["operation_mode"] = self.__createDataset__(1001, "avg")
        datasets["dc_breaker_state"] = self.__createDataset__(1002, "avg")
        datasets["dc_relay_state"] = self.__createDataset__(1003, "sum")
        datasets["ac_relay_state"] = self.__createDataset__(1004, "sum")
        datasets["temp1"] = self.__createDataset__(1005, "avg")
        datasets["temp_day_min"] = self.__createDataset__(1006, "avg")
        datasets["temp_day_max"] = self.__createDataset__(1007, "avg")
        datasets["dc_temp_target"] = self.__createDataset__(1008, "avg")
        datasets["ac_temp_target"] = self.__createDataset__(1009, "avg")
        datasets["tempchip"] = self.__createDataset__(1010, "avg")
        datasets["iso_voltage"] = self.__createDataset__(1011, "avg")
        datasets["dc_voltage"] = self.__createDataset__(1012, "avg")
        datasets["dc_current"] = self.__createDataset__(1013, "avg")
        datasets["dc_power"] = self.__createDataset__(1014, "sum")
        datasets["dc_day_wh"] = self.__createDataset__(1015, "avg")
        datasets["dc_total_kwh"] = self.__createDataset__(1016, "avg")
        datasets["ac_day_wh"] = self.__createDataset__(1017, "avg")
        datasets["minutes_from_noon"] = self.__createDataset__(1018, "avg")
        datasets["minutes_since_dusk"] = self.__createDataset__(1019, "avg")
        datasets["ac_boost_mode"] = self.__createDataset__(1020, "avg")
        datasets["temp2"] = self.__createDataset__(1021, "avg")
        datasets["boost_temp_target"] = self.__createDataset__(1022, "avg")
        datasets["ww2offset_calibration"] = self.__createDataset__(1023, "avg")
        return datasets

# Entry Point     
if __name__ == "__main__":

    from ACThor import ACThor

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.DEBUG)

    device = ACThor("120100200505tes1")
    device.setHost("192.168.92.29")
    register = device.readRegister(1000)
    print(register)
    registers = device.readRegisters(1000, 80)
    print(str(registers))

    device.writeRegister(1000, 55)