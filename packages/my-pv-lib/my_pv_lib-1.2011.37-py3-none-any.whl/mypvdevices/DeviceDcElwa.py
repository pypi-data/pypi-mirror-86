#!/usr/bin/python

from colr import color
from datetime import datetime, timedelta
import logging
import time
import json

from mypvdevices.Device import Device
from mypvdevices.ModbusConnection import ModbusConnection

MODBUSWARNLEVEL = 0.5
REGISTERTIMEOUT = 5
BUILDNR = "4321"

class DeviceDcElwa(Device):
    __firmwareVersion__ = "1." + str(BUILDNR)
    __deviceType__ = "ELWA"

    def __init__(self, serial, nodeId):
        self.__nodeId__ = nodeId
        Device.__init__(self, serial)

    def getIdentifier(self):
        return self.getSerial() + ", Node: " + str(self.__nodeId__)

    def __createSetup__(self):
        return {
            "device": self.__deviceType__, \
            "fwversion": self.__firmwareVersion__, \
            "serialno": self.__serial__, \
            "elno": self.__nodeId__, \
            "ww2target": None, \
            "ww2offset": 1514
            }

    def __getSettingsMap__(self):
        settings = {
            "ww2target": {
                "register": 1022,   #ELWA Modbus Interface boost temperature
                "forced": False
            },
            "ww2offset": {
                "register": 1023,   #Temp sensor offset calibration
                "forced": True
            }
        }
        return settings

    def getData(self):

        acRelayState = self.getDataset("ac_relay_state")
        dcPower = self.getDataset("dc_power")
        operationMode = self.getDataset("operation_mode")

        if operationMode == 3 or operationMode == 5 or operationMode == 6 or operationMode == 7 or operationMode == 8 or operationMode == 9 or operationMode == 10 or operationMode == 11 or operationMode == 12 or operationMode == 13 or operationMode == 14 or operationMode == 15 or operationMode == 16 or operationMode == 20 or operationMode == 21 or operationMode == 135:
            acHeating = True
        else:
            acHeating = False

        if acRelayState != None:
            if acHeating == True and acRelayState == 1:
                boostpower = 750
            else:
                boostpower = 0
        else:
            boostpower = None

        if(boostpower != None):
            power = (int(dcPower) + int(boostpower))
            meter = -boostpower
        else:
            power = dcPower
            meter = None

        data={
            "device": self.__deviceType__,
            "fwversion": self.__firmwareVersion__,
            "loctime": time.strftime("%H:%M:%S"),
            "dev_id": self.__nodeId__,
            "day_counter" : self.getDataset("day_counter"),
            "op_mode": operationMode,
            "dc_breaker": self.getDataset("dc_breaker_state"),
            "dc_relay": self.getDataset("dc_relay_state"),
            "ac_relay": acRelayState,
            "temp1": self.getDataset("temp1"),
            "temp_day_min": self.getDataset("temp_day_min"),
            "temp_day_max": self.getDataset("temp_day_max"),
            "ww1target": self.getDataset("dc_temp_target"),
            "ac_temp_target": self.getDataset("ac_temp_target"),
            "tempchip": self.getDataset("tempchip"),
            "iso_voltage": self.getDataset("iso_voltage"),
            "dc_voltage": self.getDataset("dc_voltage"),
            "dc_current": self.getDataset("dc_current"),
            "power_elwa": power,
            "boostpower_elwa": boostpower,
            "dc_day_wh": self.getDataset("dc_day_wh"),
            "dc_total_kwh": self.getDataset("dc_total_kwh"),
            "ac_day_wh": self.getDataset("ac_day_wh"),
            "minutes_from_noon": self.getDataset("minutes_from_noon"),
            "minutes_since_dusk": self.getDataset("minutes_since_dusk"),
            "ac_boost_mode": self.getDataset("ac_boost_mode"),
            "m1sum": dcPower,
            "m0sum": meter,
            "temp2": self.getDataset("temp2"),
            "ww2target": self.getDataset("boost_temp_target"),
            "ww2offset": self.getDataset("ww2offset_calibration"),
            "modbuserrorrate":  self.getCommunicationErrorsRate()
            }            
        return data

    def getLogData(self):

        acRelayState = self.getLogValue("ac_relay_state")
        if acRelayState != None:
            boostpower = int(round(acRelayState*750))
        else:
            boostpower = None
        
        dcPower = self.getIntLogValue("dc_power")
        if dcPower != None:
            if(boostpower != None):
                power = int(dcPower + boostpower)
            else:
                power = dcPower
        else:
            power = None
        if(boostpower != None):
            metercons = -boostpower
        else:
            metercons = None

        pvprod = dcPower

        sLog={
			"modbus_error_rate" : self.getCommunicationErrorsRate(),
			"day_counter" : self.getIntLogValue("day_counter"),
			"op_mode": self.getIntLogValue("operation_mode"),
			"dc_breaker": self.getIntLogValue("dc_breaker_state"),
			"dc_relay": self.getIntLogValue("dc_relay_state"),
			"ac_relay": self.getIntLogValue("ac_relay_state"),
			"temp": self.getIntLogValue("temp1"),
			"temp_day_min": self.getIntLogValue("temp_day_min"),
			"temp_day_max": self.getIntLogValue("temp_day_max"),
			"dc_temp_target": self.getIntLogValue("dc_temp_target"),
			"ac_temp_target": self.getIntLogValue("ac_temp_target"),
			"temp_internal": self.getIntLogValue("tempchip"),
			"iso_voltage": self.getIntLogValue("iso_voltage"),
			"dc_voltage": self.getIntLogValue("dc_voltage"),
			"dc_current": self.getIntLogValue("dc_current"),
			"dc_power": self.getIntLogValue("dc_power"),
			"dc_day_wh": self.getIntLogValue("dc_day_wh"),
			"dc_total_kwh": self.getIntLogValue("dc_total_kwh"),
			"ac_day_wh": self.getIntLogValue("ac_day_wh"),
			"minutes_from_noon": self.getIntLogValue("minutes_from_noon"),
			"minutes_since_dusk": self.getIntLogValue("minutes_since_dusk"),
			"ac_boost_mode": self.getIntLogValue("ac_boost_mode"),
			"temp2": self.getIntLogValue("temp2"),
			"ww2target": self.getIntLogValue("boost_temp_target"),
			"ww2offset": self.getIntLogValue("ww2offset_calibration"),
        }

        logData = { 
            "i_power": power,
            "i_boostpower": boostpower,
            "i_m1sum": pvprod,
            "i_metercons": metercons,
            "i_temp1": self.getIntLogValue("temp1"),
            "i_temp2": self.getIntLogValue("temp2"),
            "s_json" : json.dumps(sLog)
        }

        ModbusConnection.instance().resetCounters(self.__nodeId__)
        self.__logData__.clear()
        return logData

    def __checkRegiterTimeStamp__(self):
        if self.__registerLastSuccessfullReadTimeStamp__ != None:
            difference = time.time() - self.__registerLastSuccessfullReadTimeStamp__
            if(difference > REGISTERTIMEOUT):
                return False
            return True
        else:
            return False
    
    def __supervise__(self):
        
        value = self.getDataset("temp1")
        if value != None and ( value > 1200 or value < 0 ):
            logging.error("[Device] " + self.getIdentifier() + " - Temp1 sensor error: " + str(value))
            temp1error = True
        else:
            temp1error = False

        value = self.getDataset("temp2")
        if value != None and ( value > 1200 or value < 0 ):
            logging.error("[Device] " + self.getIdentifier() + " - Temp2 sensor error: " + str(value))
            temp2error = True
        else:
            temp2error = False

        value = self.getDataset("tempchip")
        if value == 0 :
            logging.error("[Device] " + self.getIdentifier() + " - No IR Connection to Device.")
            irError = True
        else:
            irError = False

        value = self.getDataset("operation_mode")
        if value != None and value > 100 :
            logging.error("[Device] " + self.getIdentifier() + " - Operation Mode " + str(value) + " detected.")
            opmodeError = True
        else:
            opmodeError = False

        modbusErrorRate = self.getCommunicationErrorsRate()
        if modbusErrorRate != None and modbusErrorRate > MODBUSWARNLEVEL and modbusErrorRate < 1:
            logging.error("[Device] " + self.getIdentifier() + " - Modbus error rate to hight " + str(modbusErrorRate) + ".")
            modbusWarning = True
        else:
            modbusWarning = False
        if modbusErrorRate == 1 :
            logging.error("[Device] " + self.getIdentifier() + " - Modbus communication to device not working.")
            modbusError = True
        else:
            modbusError = False

        if self.__checkRegiterTimeStamp__() != True:
            logging.error("[Device] " + self.getIdentifier() + " - Register values to old. Communication errors expected.")
            registerError = True
        else:
            registerError = False

        healthState = 0

        #healthState warnings
        if temp2error == True or irError == True or opmodeError == True or modbusWarning == True:
            healthState = 1

        #healthState errors
        if temp1error == True or modbusError == True or registerError == True:
            healthState = 2

        self.__setHealthState__(healthState)

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

    from mypvdevices.DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.DEBUG)

    serial = "120100200505tes1"
    cryptoKey = "ABABABABABABABAB"
    serial2 = "120100200505tes2"
    cryptoKey2 = "ABABABABABABABAB"
    serial3 = "120100200505tes3"
    cryptoKey3 = "ABABABABABABABAB"
    server = "my-pv.live"

    # try to read from valid device
    device = DeviceDcElwa(serial, 1)
    try:
        device.__readRegisters__()
        if(len(device.__registers__) == 24):
            print(color('SUCCESS: reading registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid length")
    except Exception as e:
        print(color('ERROR: reading registers. ' + str(e), fore='red', style='bright'))

    try:
        if device.__syncSettings__():
            print(color('SUCCESS: syncing settings.', fore='green', style='bright'))
        else:
            raise Exception("settings sync failed")
    except Exception as e:
        print(color('ERROR: syncing settings. ' + str(e), fore='red', style='bright'))

    try:
        device.__processRegisters__()
        value = device.getDataset("dc_power")
        if( value != None ):
            print(color('SUCCESS: processing registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers. ' + str(e), fore='red', style='bright'))

    try:
        value = device.getDataset("seppi")
        if( value == None ):
            print(color('SUCCESS: getting value of unkown registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: getting value of unkown registers. ' + str(e), fore='red', style='bright'))

    time.sleep(2)
    device.__processRegisters__()
    time.sleep(2)

    device.__readRegisters__()
    try:
        device.__processRegisters__()
        value = device.getLogValue("dc_power")
        if( value != None ):
            print(color('SUCCESS: processing registers again.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers again. ' + str(e), fore='red', style='bright'))

    
    data = device.getData()
    if(data != None and data != {}):
        print(color('SUCCESS: getting getData.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting getData.', fore='red', style='bright'))

    logData = device.getLogData()
    if(logData != None and logData != {}):
        print(color('SUCCESS: getting getLogData.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting getLogData.', fore='red', style='bright'))

    key = "ww2target"
    targetValue = 500
    if(device.setSetupValue(key, targetValue)):
        print(color('SUCCESS: sending setup value to device.', fore='green', style='bright'))
    else:
        print(color('ERROR: sending setup value to device.', fore='red', style='bright'))

    setup = device.getSetup()
    if(setup[key] == targetValue):
        print(color('SUCCESS: Setting setup value.', fore='green', style='bright'))
    else:
        print(color('ERROR: Setting setup value.', fore='red', style='bright'))


    input("Press ENTER to start running tests")
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceDcElwa(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addConnection(connection)
    device.start()

    try:
        while True:
            print(color('[Device] test active. Press CTRL+C to stop', fore='blue', style='bright'))
            device.showInfo()
            device.showCommunicationErrors()
            device.showCommunicationErrorsRate()
            device.__supervise__()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[Device] Stopping Test...")
        device.stop()

    input("Press ENTER to start communication tests")

    #DCS communication tests
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceDcElwa(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addConnection(connection)
    # device.setLogDataSendInterval(5)

    device2 = DeviceDcElwa(serial2, 2)
    connection2 = DcsConnection(serial2, cryptoKey2, server, 50333)
    device2.addConnection(connection2)

    device3 = DeviceDcElwa(serial3, 7)
    connection3 = DcsConnection(serial3, cryptoKey3, server, 50333)
    device3.addConnection(connection3)

    device.start()
    device2.start()
    device3.start()
    try:
        while True:
            print(color('[Device] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            # device.showInfo()
            device.showCommunicationErrors()
            device.showCommunicationErrorsRate()
            device2.showCommunicationErrors()
            device2.showCommunicationErrorsRate()
            device3.showCommunicationErrors()
            device3.showCommunicationErrorsRate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
        device2.stop()
        device3.stop()
    input("waiting...")
