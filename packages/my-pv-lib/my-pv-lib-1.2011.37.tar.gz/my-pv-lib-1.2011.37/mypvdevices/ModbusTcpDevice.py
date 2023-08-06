#!/usr/bin/python

import logging
import threading
from pyModbusTCP.client import ModbusClient

from Device import Device

class ModbusTcpException(Exception):
    def __init__(self, msg, code):
        self.code = code
        self.message = msg
    def __str__(self):
        return repr(self.message)

class ModbusTcpDevice(Device):
    __deviceType__ = "ModbusTcpDevice"
    __mutex__ = threading.Lock()
    __modbusClient__ = None
    __host__ = None

    def __init__(self, serial):
        Device.__init__(self, serial)

    def setHost(self, hostname):
        logging.debug(self.getIdentifier() + " Setting host to " + str(hostname))

        if hostname == None:
            msg="hostname required"
            logging.debug(self.getIdentifier() + ": " + str(msg))
            raise TypeError(msg)

        if not isinstance(hostname, str):
            msg="hostname hast to be a string"
            logging.debug(self.getIdentifier() + ": " + str(msg))
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
            registers = None
            if self.__modbusClient__ != None:
                logging.debug(self.getIdentifier() + " Host: " + str(self.__modbusClient__.host()) + ": Reading " + str(registersToRead) +" registers starting with register "+ str(startRegisterAddress))
                registers = dict()
                try:
                    modbus_response = self.__modbusClient__.read_holding_registers(startRegisterAddress, registersToRead)
                    if modbus_response == None:
                        raise Exception("No data received.")

                    logging.debug(self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + ": Data: " + str(modbus_response))
                    for i in range(len(modbus_response)):
                        registers[startRegisterAddress + i] = modbus_response[i]
                except Exception as e:
                    logging.warning(self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + " Modbus read error: " + str(e))
                    registers = None
            else:
                logging.error(self.getIdentifier() + ": no Modbus-Client ")
        return registers

    def readRegister(self, registerAddress):
        with self.__mutex__:
            register = None
            if self.__modbusClient__ != None:
                logging.debug(self.getIdentifier() + " Host: " + str(self.__modbusClient__.host()) + ": Reading register " + str(registerAddress))
                try:
                    modbus_response = self.__modbusClient__.read_holding_registers(registerAddress, 1)
                    if modbus_response == None:
                        errorcode = self.__modbusClient__.last_error()

                        if errorcode == 2:
                            raise ModbusTcpException("Host not reachable " + str(self.__modbusClient__.host()), errorcode)
                        elif errorcode == 4:
                            raise ModbusTcpException("Invalid Register " + str(registerAddress), errorcode)
                        else:
                            raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

                    logging.debug(self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + ": Data: " + str(modbus_response))
                    register = modbus_response[0]
                except Exception as e:
                    logging.warning(self.getIdentifier() + ": Host: " + str(self.__modbusClient__.host()) + " Modbus read error: " + str(e))
                    raise e
            else:
                logging.error(self.getIdentifier() + ": no Modbus-Client ")
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
            logging.debug(self.getIdentifier() + ": writing register " + str(registerId) +" with value "+ str(value))
            if self.__modbusClient__ != None:
                try:
                    result = self.__modbusClient__.write_single_register(registerId, value)
                    if result == None:
                        logging.warning(self.getIdentifier() + " Cannot write register. Register " + str(registerId))
                except Exception as e:
                    logging.warning(self.getIdentifier() + " Modbus Write Error: " + str(e))
                    result = None
        return result

    def discoverDevice(self):
        return "192.168.92.29"

# Entry Point     
if __name__ == "__main__":

    from ModbusTcpDevice import ModbusTcpDevice

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.DEBUG)

    device = ModbusTcpDevice("120100200505tes1")
    device.setHost("192.168.92.29")
    try:
        register = device.readRegister(2000)
        print(register)
    except Exception as e:
        pass
    register = device.readRegister(1001)
    print(register)
    device.setHost("192.168.92.26")
    try:
        register = device.readRegister(1001)
        print(register)
    except Exception as e:
        if e.code == 2:
            print("Fixing host")
            host = device.discoverDevice()
            if host != None:
                device.setHost(host)
    try:
        register = device.readRegister(1001)
        print(register)
    except Exception as e:
        if e.code == 2:
            print("host cannot be fixed")
        
    # registers = device.readRegisters(1000, 80)
    # print(str(registers))

    # device.writeRegister(1000, 55)

    # print(str(device.getSetup()))

    # print(str(device.getData()))

    # print(str(device.getLogData()))