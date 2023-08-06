#!/usr/bin/python

from _pytest.compat import STRING_TYPES
from colr import color
from datetime import datetime, timedelta
import logging
import time
import threading
import json
from pyModbusTCP.client import ModbusClient

from mypvdevices.Device import Device
# from mypvdevices.ModbusConnection import ModbusConnection

BUILDNR = "4321"

class ACThor(Device):
    __firmwareVersion__ = "1." + str(BUILDNR)
    __deviceType__ = "AC Thor"
    __mutex__ = threading.Lock()
    __modbusClient__ = None
    __host__ = None

    def __init__(self, serial):
        Device.__init__(self, serial)
        # self.__modbusClient__ = ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = 1, bytesize = 8, parity = 'N', baudrate= 9600, timeout=0.5, retry_on_empty=True, retry_on_invalid=True)

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

    def setHost(self, hostname):
        logging.debug("[ACThor] " + self.getIdentifier() + " Setting host to " + str(hostname))

        if hostname == None:
            msg="hostname required"
            logging.debug("[ACThor] " + self.getIdentifier() + ": " + str(msg))
            raise TypeError(msg)

        if not isinstance(hostname, str):
            msg="hostname hast to be a string"
            logging.debug("[ACThor] " + self.getIdentifier() + ": " + str(msg))
            raise TypeError(msg)

        self.__host__ = hostname

        if self.__modbusClient__ == None:
            try:
                self.__modbusClient__ = ModbusClient(host=self.__host__, port=502, timeout=5, auto_open=True, auto_close=True)
            except ValueError:
                print("Error with host or port params")
        else:
            self.__modbusClient__.host(self.__host__)

    def readRegisters(self, startRegisterAddress, registersToRead):
        with self.__mutex__:
            registers = dict()
            if self.__modbusClient__ != None:
                logging.debug("[ACThor] " + self.getIdentifier() + " Host: " + str(self.__modbusClient__.host()) + ": Reading " + str(registersToRead) +" registers starting with register "+ str(startRegisterAddress))
                try:
                    modbus_response = self.__modbusClient__.read_holding_registers(startRegisterAddress, registersToRead)
                    if modbus_response == None:
                        raise Exception("No data received.")

                    logging.debug("[ACThor] " + self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + ": Data: " + str(modbus_response))
                    for i in range(len(modbus_response)):
                        registers[startRegisterAddress + i] = modbus_response[i]
                except Exception as e:
                    logging.warning("[ACThor] " + self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + " Modbus read error: " + str(e))
                    registers = None
            else:
                logging.error("[ACThor] " + self.getIdentifier() + ": no Modbus-Client ")
        return registers

    def readRegister(self, registerAddress):
        with self.__mutex__:
            register = None
            if self.__modbusClient__ != None:
                logging.debug("[ACThor] " + self.getIdentifier() + " Host: " + str(self.__modbusClient__.host()) + ": Reading register " + str(registerAddress))
                try:
                    modbus_response = self.__modbusClient__.read_holding_registers(registerAddress, 1)
                    if modbus_response == None:
                        raise Exception("No data received.")

                    logging.debug("[ACThor] " + self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + ": Data: " + str(modbus_response))
                    register = modbus_response[0]
                except Exception as e:
                    logging.warning("[ACThor] " + self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + " Modbus read error: " + str(e))
            else:
                logging.error("[ACThor] " + self.getIdentifier() + ": no Modbus-Client ")
        return register

    def writeRegister(self, registerId, value):
        if registerId == None:
            msg="registerId required"
            raise TypeError(msg)

        if not isinstance(registerId, int):
            msg="registerId hast to be a int"
            raise TypeError(msg)

        if value == None:
            msg="value required"
            raise TypeError(msg)

        if not isinstance(value, int):
            msg="value hast to be a int"
            raise TypeError(msg)

        result = None
        with self.__mutex__:
            logging.debug("[ACThor] " + self.getIdentifier() + ": writing register " + str(registerId) +" with value "+ str(value))
            if self.__modbusClient__ != None:
                try:
                    result = self.__modbusClient__.write_single_register(registerId, value)
                    if result == None:
                        logging.warning("[ACThor] " + self.getIdentifier() + " Cannot write register. Register " + str(registerId))
                except Exception as e:
                    logging.warning("[ACThor] " + self.getIdentifier() + " Modbus Write Error: " + str(e))
                    result = None
        return result


# Entry Point     
if __name__ == "__main__":

    from ACThor import ACThor

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.DEBUG)

    device = ACThor("120100200505tes1")
    device.setHost("192.168.92.29")
    register = device.readRegister(1000)
    print(register)
    registers = device.readRegisters(1000, 80)
    print(str(registers))

    device.writeRegister(1000, 55)