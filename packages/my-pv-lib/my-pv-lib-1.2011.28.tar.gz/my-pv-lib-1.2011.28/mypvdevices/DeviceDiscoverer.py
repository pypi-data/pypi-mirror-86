#!/usr/bin/python

import logging
import threading
import socket
# import time
# from colr import color

# BUSRECOVERYTIME = 0

class DeviceDiscoverer:     #Singleton
    __instance__ = None
    __mutex__ = threading.Lock()

    @staticmethod
    def instance():
        """ Static access method. """
        if DeviceDiscoverer.__instance__ == None:
            with DeviceDiscoverer.__mutex__:
                DeviceDiscoverer()
        return DeviceDiscoverer.__instance__

    def __init__(self):
        """ Virtually private constructor. """
        if DeviceDiscoverer.__instance__ != None:
            raise Exception("[DeviceDiscoverer] This class is a singleton! Instance already created")
        else:
            DeviceDiscoverer.__instance__ = self

        # self.__connectionErrorCounter__ = dict()
    
    def searchDevices(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        s.settimeout(5)

        crc = B'\x84db'
        id = B'\x4f4c'
        string = "AC-THOR 9s".encode('utf-8')
        missingString = 16 - len(string)
        string = string + B'\x00' * missingString
        data = crc + id + string
        missingData = 32 - len(data)
        data = data + B'\x00' * missingData

        print("data len: " + str(len(data)))

        s.sendto(data, ("<broadcast>", 16124))
        try:
            print("Response: %s" % s.recv(1024))
        except socket.timeout:
            print("No server found")

        s.close()


# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    DeviceDiscoverer.instance().searchDevices()

    # trying to use modbus module
    # socket = ModbusConnection.instance().__connectSocket__()
    # if(socket == True):
    #     print(color('SUCCESS: Using modbus module.', fore='green', style='bright'))
    # else:
    #     print(color('ERROR: Using modbus module.', fore='red', style='bright'))
    #     input("PRESS ENTER TO CONTINUE TESTING")
        