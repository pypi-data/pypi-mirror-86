#!/usr/bin/python

import logging
import threading
import time
from datetime import datetime
import statistics
from colr import color

from mypvdevices.ModbusConnection import ModbusConnection

BUILDNR = "1.2011.37"

JOINTIMEOUT = 5
SERIALLEN = 16
DEVICESLEEPTIME = 5
DEFAULTMODBUSFREQUENCY = 3

class Device:
    __firmwareVersion__ = "1." + str(BUILDNR)
    __deviceType__ = "Dummy-Device"
    __lock__ = None
    __running__ = False
    __serial__ = None
    __monitorThread__ = None
    __datasets__ = None
    __data__ = None
    __logData__ = None
    __logDataTimeStamp__ = None
    __logDataCounter__ = None
    __logDataLastValue__ = None
    __logDataSum__ = None
    __connections__ = None
    __setup__ = None
    __registers__ = None
    __registerTimeStamp__ = None
    __modbusThread__ = None
    __settingsMap__ = None
    __nodeId__ = None
    __modbusFrequency__ = DEFAULTMODBUSFREQUENCY
    __startRegister__ = 1000
    __registersToRead__ = 24
    __lastLogDataSendTime__ = None
    __logDataSendInterval__ = 0
    __modBusExecuted__ = None
    __healthState__ = 0
    __registerLastSuccessfullReadTimeStamp__ = None

    def __init__(self, serial):
        if serial != None and len(serial) == SERIALLEN:
            self.__serial__ = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)
            
        self.__lock__ = threading.Lock()
        self.__connections__ = list()
        self.__registers__ = dict()
        self.__data__ = dict()
        self.__logData__ = dict()
        self.__logDataCounter__ = dict()
        self.__logDataLastValue__ = dict()
        self.__logDataSum__ = dict()
        self.__datasets__ = self.__getRegisterMapping__()
        self.__setup__ = self.__createSetup__()
        self.__settingsMap__ = self.__getSettingsMap__()
        logging.debug("new "+str(self.__deviceType__)+" created. Serial: " + str(self.__serial__))

    def addConnection(self, connection):
        if(connection != None):
            if(connection.addDevice(self)):
                self.__connections__.append(connection)
                logging.debug("[Device] ID " + str(self.__serial__) + " Added connection to device")
            else:
                logging.error("[Device] ID " + str(self.__serial__) + " Failed adding connection to device")

    def start(self):
        self.__running__ = True
        logging.debug("[Device] ID " + str(self.__serial__) + " starting...")
        self.__modbusThread__ = threading.Thread(target=self.__runModbus__, name="Modbus " + str(self.__serial__))
        self.__modbusThread__.start()
        self.__monitorThread__ = threading.Thread(target=self.__run__, name="Monitor " + str(self.__serial__))
        self.__monitorThread__.start()
        time.sleep(1)
        for connection in self.__connections__:
            connection.connect()
        logging.debug("[Device] ID " + str(self.__serial__) + " started.")
    
    def stop(self):
        self.__running__ = False
        logging.info("[Device] ID " + str(self.__serial__) + " stopping.")
        if(self.__modbusThread__ != None and self.__modbusThread__.is_alive()):
            self.__modbusThread__.join(JOINTIMEOUT)
        for connection in self.__connections__:
            connection.disconnect()
    
    def getSerial(self):
        return self.__serial__

    def getIdentifier(self):
        return self.getSerial()

    def getState(self):
        return self.__running__
    
    def getDeviceType(self):
        return self.__deviceType__

    def getSetup(self): 
        return self.__setup__

    def setSetupValue(self, key, value):
        logging.info("Setup Change: key="+str(key)+", value="+str(value))
        try:
            self.__setup__[key] = value
            if key in self.__settingsMap__:
                register = self.__settingsMap__[key]["register"]
                self.__writeRegister__(register, value)
            else:
                raise Exception("no register mapping found.")

            registervalue = ModbusConnection.instance().readRegisters(self.__nodeId__, register, 1)
            if registervalue[register] != value:
                logging.info("[Device] ID " + str(self.__serial__) + " Register verification failed. " + str(registervalue[register]))
                return False

            return True
        except Exception as e:
            logging.info("[Device] ID " + str(self.__serial__) + " Setup change not successfull. " + str(e))
            return False

    def setModbusFrequency(self, frequency):
        if frequency != None and frequency >= 0 and frequency < 90000:
            self.__modbusFrequency__ = frequency
            logging.info("[Device] ID " + str(self.__serial__) + " modbus frequency set to " + str(self.__modbusFrequency__))
            return True
        else:
            logging.info("[Device] ID " + str(self.__serial__) + " set modbus frequency failed. Out of range: " + str(frequency))
            return False

    def setLogDataSendInterval(self, interval):
        if interval != None and interval >= 0 and interval < 90000:
            self.__logDataSendInterval__ = interval
            logging.info("[Device] ID " + str(self.__serial__) + " logdata send interval set to " + str(self.__modbusFrequency__))
            return True
        else:
            logging.info("[Device] ID " + str(self.__serial__) + " set logdata send interval failed. Out of range: " + str(interval))
            return False

    def setStartRegister(self, startRegister):
        if startRegister != None and startRegister >= 0 and startRegister < 10000:
            self.__startRegister__ = startRegister
            logging.info("[Device] ID " + str(self.__serial__) + " start-register set to " + str(self.__startRegister__))
            return True
        else:
            logging.info("[Device] ID " + str(self.__serial__) + " set start-register failed. Out of range: " + str(startRegister))
            return False

    def setRegistersToRead(self, registersToRead):
        if registersToRead != None and registersToRead > 0 and registersToRead < 10000:
            self.__registersToRead__ = registersToRead
            logging.info("[Device] ID " + str(self.__serial__) + " registersToRead set to " + str(self.__registersToRead__))
            return True
        else:
            logging.info("[Device] ID " + str(self.__serial__) + " set registersToRead failed. Out of range: " + str(registersToRead))
            return False

    def __run__(self):
        while self.__running__:
            logging.debug("[Device] ID " + str(self.__serial__) + " monitor running...")
            if not self.__modbusThread__.is_alive():
                logging.error("[Device] ID " + str(self.__serial__) + " Modbus-Thread not alive!")
            for connection in self.__connections__:
                try:
                    connection.watchdog()
                except:
                    logging.error("[Device] ID " + str(self.__serial__) + " watchdog failed.")

            if self.__logDataSendInterval__ > 0:
                if self.__lastLogDataSendTime__ == None:
                    self.__lastLogDataSendTime__ = datetime.now()
                else:
                    difference = datetime.now() - self.__lastLogDataSendTime__
                    if(difference.total_seconds() > self.__logDataSendInterval__):
                        for connection in self.__connections__:
                            try:
                                connection.loadLogData()
                                connection.sendLogData()
                                self.__lastLogDataSendTime__ = datetime.now()
                                logging.info("[Device] ID " + str(self.__serial__) + " active sent logData to server: " + str(connection.getServer()))
                            except Exception as e:
                                logging.warning("[Device] ID " + str(self.__serial__) + " active sending logData to server " + str(connection.getServer()) + " failed. " + str(e))
            try:
                self.__supervise__()
            except Exception as e:
                logging.warning("[Device] ID " + str(self.__serial__) + " supervision failed failed. " + str(e))

            if self.__modBusExecuted__ != None:
                difference = datetime.now() - self.__modBusExecuted__
                if(difference.total_seconds() > self.__modbusFrequency__ * 3):
                    if self.__datasets__ != None:
                        for dataset in self.__datasets__:
                            self.__data__[dataset] = None

            time.sleep(DEVICESLEEPTIME)

    def __supervise__(self):
        logging.info("[Device] " + self.getIdentifier() + ": everything ok.")

    def __setHealthState__(self, state):
        if state != None and state <= 3 and state >= 0:
            if self.__healthState__ != state:
                self.__healthState__ = state
                logging.info("[Device] " + self.getIdentifier() + ". HealthState set to " + str(state))
        else:
            logging.error("[Device] " + self.getIdentifier() + ". Cannot set healthState. Invalid state: " + str(state))
            raise Exception("invalid state " + str(state))

    def getHealthState(self):
        return self.__healthState__

    def __runModbus__(self):
        while self.__running__:
            try:
                self.__modBusExecuted__ = datetime.now()
                self.__excecuteModbus__()
            except Exception as e:
                logging.error("[Device] " + self.getIdentifier() + ". Modbus Thread Error: " + str(e))

    def __excecuteModbus__(self):
        if self.__modbusFrequency__ > 0:
            logging.debug("[Device] ID " + str(self.__serial__) + " Modbus running...")
            self.__readRegisters__()
            if self.__registers__ != None:
                if len(self.__registers__) > 0:
                    self.__syncSettings__()
                    self.__processRegisters__()
                else:
                    logging.error("[Device] " + self.getIdentifier() + ". No bus communication to device.")
            else:
                logging.debug("[Device] " + self.getIdentifier() + ". No registers to process.")
            time.sleep(self.__modbusFrequency__)

    def __syncSettings__(self):
        errors = 0
        if self.__settingsMap__ != None:
            for name in self.__settingsMap__:
                if self.__settingsMap__[name]["register"] in self.__registers__:
                    if name in self.__setup__:
                        if self.__registers__[self.__settingsMap__[name]["register"]] != self.__setup__[name]:
                            logging.info("[Device] ID " + str(self.__serial__) + " setting missmatch " + str(name) + " - Device: " + str(self.__registers__[self.__settingsMap__[name]["register"]]) + "; Setup: " + str(self.__setup__[name]) + ".")
                            if self.__settingsMap__[name]["forced"]:
                                self.__writeRegister__(self.__settingsMap__[name]["register"], self.__setup__[name])
                                logging.info("[Device] ID " + str(self.__serial__) + " forcing " + str(name) + " to "+str(self.__setup__[name])+".")
                            else:
                                self.__setup__[name] = self.__registers__[self.__settingsMap__[name]["register"]]
                                self.sendSetup()
                                logging.debug("[Device] ID " + str(self.__serial__) + " changed setup. " + str(name) + "=" + str(self.__setup__[name]) + ".")
                    else:
                        logging.warning("[Device] ID " + str(self.__serial__) + " setting element " + str(name) + " not found in setup.")
                        errors += 1
                else:
                    logging.warning("[Device] ID " + str(self.__serial__) + " register for setting " + str(name) + " not found.")
                    errors += 1
        if errors == 0:
            return True
        else:
            return False

    def sendSetup(self):
        success = True
        for connection in self.__connections__:
            if connection.isConnected():
                try:
                    connection.sendSetup()
                except:
                    logging.error("[Device] ID " + str(self.__serial__) + " cannot send setup change to server.")
                    success = False
        return success

    def __readRegisters__(self):
        self.__lock__.acquire()
        if self.__startRegister__ != None and self.__registersToRead__ != None:
            logging.debug("[Device] ID " + str(self.__serial__) + " reading " + str(self.__registersToRead__) + " registers starting with " + str(self.__startRegister__))
            if self.__nodeId__ != None:
                registers = ModbusConnection.instance().readRegisters(self.__nodeId__, self.__startRegister__, self.__registersToRead__)
                self.__registers__ = registers
                self.__registerTimeStamp__ = time.time()
                if registers != None and len(registers) > 0:
                    self.__registerLastSuccessfullReadTimeStamp__ = time.time()
                # else:
                #     logging.debug("[Device] ID " + str(self.__serial__) + " cannot read registers")
            else:
                logging.info("[Device] ID " + str(self.__serial__) + " creating dummy data for " + str(self.__registersToRead__) + " registers")
                if self.__registers__ != None:
                    self.__registers__.clear()
                for i in range(self.__registersToRead__):
                    self.__registers__[self.__startRegister__ + i] = i*1000
                    if(i == 3):
                        self.__registers__[self.__startRegister__ + i] = None
                    if(i == 5):
                        self.__registers__[self.__startRegister__ + i] = 65
                    if(i == 13):
                        self.__registers__[self.__startRegister__ + i] = 1000
                    if(i == 21):
                        self.__registers__[self.__startRegister__ + i] = datetime.now().minute
                self.__registerTimeStamp__ = time.time()
        else:
            logging.warning("[Device] ID " + str(self.__serial__) + " no registers to read")
        self.__lock__.release()

    def __writeRegister__(self, registerId, valueToWrite):
        self.__lock__.acquire()
        logging.debug("[Device] ID " + str(self.__serial__) + " writing register " + str(registerId) + " value: " + str(valueToWrite))
        if self.__nodeId__ != None:
            ModbusConnection.instance().writeRegister(self.__nodeId__, registerId, valueToWrite)
        else:
            print("Register " + str(registerId) + " changed to " + str(valueToWrite))
        self.__lock__.release()

    def getRegisterValue(self, registerId):
        self.__lock__.acquire()
        try:
            if(self.__registers__[registerId] != None):
                value = {
                    "time": self.__registerTimeStamp__,
                    "value": self.__registers__[registerId]
                }
            else:
                value = None
        except:
            logging.warning("[Device] ID " + str(self.__serial__) + " register not found " + str(registerId))
            value = None
        self.__lock__.release()
        return value

    def __processRegisters__(self):
        if self.__datasets__ != None:
            for dataset in self.__datasets__:
                registerId = self.__datasets__[dataset][0]
                register = self.getRegisterValue(registerId)

                if register != None:
                    value = register["value"]
                    self.__data__[dataset] = value
                    self.__addToLogData__(dataset, register)
                    logging.debug("[Device] ID " + str(self.__serial__) + ", dataset=" + str(dataset) + ", value=" + str(value) + " processed")
                else:
                    logging.debug("[Device] ID " + str(self.__serial__) + " no value for dataset " + str(dataset))
                    self.__data__[dataset] = None
        else:
            logging.warning("[Device] ID " + str(self.__serial__) + " no datasets defined")
        self.__logDataTimeStamp__ = self.__registerTimeStamp__

    def __addToLogData__(self, datasetName, register):
        datasetType = self.__datasets__[datasetName][1]
        value = None
        if register["value"] != None:
            if(datasetType == "avg"):
                try:
                    self.__logDataCounter__[datasetName] = self.__logDataCounter__[datasetName] + 1
                except:
                    self.__logDataCounter__[datasetName] = 1
                try:
                    self.__logDataSum__[datasetName] = self.__logDataSum__[datasetName] + register["value"]
                except:
                    self.__logDataSum__[datasetName] = register["value"]
                value = self.__logDataSum__[datasetName] / self.__logDataCounter__[datasetName]
            if(datasetType == "sum"):
                try:
                    oldvalue = self.__logData__[datasetName]
                except:
                    oldvalue = 0
                try:
                    x0 = self.__logDataLastValue__[datasetName]
                except:
                    x0 = 0
                if(x0 == None):
                    x0 = 0
                t0 = self.__logDataTimeStamp__
                if(t0 == None):
                    t0 = register["time"]
                x1 = register["value"]
                t1 = register["time"]
                dt = (t1 - t0)/3600
                newvalue = dt * ((x1 + x0)/2)
                value = oldvalue + newvalue
                self.__logDataLastValue__[datasetName] = x1
                # print(str(self.__serial__) + " Integrating " + str(datasetName) + ": dt="+str(round(dt, 4))+" x1="+str(round(x1, 4))+" x0="+str(round(x0, 4))+" oldvalue="+str(round(oldvalue, 4))+" newvalue="+str(round(newvalue, 4))+"  value="+str(round(value, 4)))
            self.__logData__[datasetName] = value
    
    def getDataset(self, datasetName):
        if self.__data__ == None or len(self.__data__) == 0:
            return None

        try:
            return self.__data__[datasetName]
        except:
            logging.warning("[Device] ID " + str(self.__serial__) + " dataset not found " + str(datasetName))
            return None 

    def getLogValue(self, datasetName):
        if self.__logData__ == None or len(self.__logData__) == 0:
            return None

        try:
            return self.__logData__[datasetName]
        except:
            logging.warning("[Device] ID " + str(self.__serial__) + " logvalue not found " + str(datasetName))
            return None

    def getIntLogValue(self, datasetName):
        logdata = self.getLogValue(datasetName)
        if logdata != None:
            return int(logdata)
        else:
            return None
    
    def clearLog(self):
        self.__logData__.clear()
        self.__logDataCounter__.clear()
        self.__logDataSum__.clear()
        self.__logDataTimestamp = None

    def showInfo(self):
        if self.__datasets__ != None:
            for dataset in self.__datasets__:
                logging.info("[Device] ID " + str(self.__serial__) + " " + dataset + ": Live: " + str(self.getDataset(dataset)) + ", Log: " + str(self.getLogValue(dataset)) + ", HealthState: " + str(self.getHealthState()))
        else:
            print("[Device] ID " + str(self.__serial__) + " no datasets defined")
            logging.info("[Device] ID " + str(self.__serial__) + " no datasets defined")

    def getCommunicationErrorsCounter(self):
        return ModbusConnection.instance().getModbusErrorCounter(self.__nodeId__)

    def showCommunicationErrors(self):
        logging.info("[Device] " + str(self.__serial__) + " - Communication Errors: " +  str(self.getCommunicationErrorsCounter()))

    def getCommunicationErrorsRate(self):
        return ModbusConnection.instance().getModbusErrorRate(self.__nodeId__)

    def showCommunicationErrorsRate(self):
        logging.info("[Device] " + str(self.getIdentifier()) + " - Communication error-rate: " +  str(round(self.getCommunicationErrorsRate()*100)) + "%, Errors: " +  str(self.getCommunicationErrorsCounter()))

    def __createDataset__(self, registerId, type):
        dataset = [registerId, type]
        return dataset

    #############

    def __createSetup__(self):
        return {
            "device": self.__deviceType__,
            "fwversion": self.__firmwareVersion__,
            "serialno": self.__serial__,
            "ww2target": None,
            "ww2offset": 1514
            }

    def __getSettingsMap__(self):
        settings = {
            "ww2target": {
                "register": 1022,
                "forced": False
            },
            "ww2offset": {
                "register": 1023,
                "forced": True
            },
        }
        return settings
    
    def getData(self):
        t = datetime.now()
        data = {
                "fwversion": self.__firmwareVersion__,
				"power": t.second * 100,
                "temp1": t.minute,
                "temp2": self.getDataset("temp2"),
				"loctime": time.strftime("%H:%M:%S")
                }            
        return data

    def getLogData(self):
        logData = {
            # "i_unknown": 123,
            "i_power": self.getIntLogValue("power"),
            "i_boostpower": 750,
            "i_meterfeed": None,
            "i_metercons": 4,
            "i_temp1": self.getIntLogValue("temp1"),
            "i_m0l1": 6,
            "i_m0l2": 7,
            "i_m0l3": 8,
            "i_m1sum": 9,
            "i_m1l1": 10,
            "i_m1l2": 11,
            "i_m1l3": 12,
            "i_m2sum": 13,
            "i_m2l1": 14,
            "i_m2l2": 15,
            "i_m2l3": 16,
            "i_m2soc": 17,
            "i_m3sum": 18,
            "i_m3l1": 19,
            "i_m3l2": 20,
            "i_m3l3": 21,
            "i_m3soc": 22,
            "i_m4sum": 23,
            "i_m4l1": 24,
            "i_m4l2": 25,
            "i_m4l3": 26,
            "s_json" : "27",
            "i_temp2": self.getIntLogValue("temp2"),
            "i_power1": 29,
            "i_power2": 30,
            "i_power3": 31,
            "i_temp3": 32,
            "i_temp4": 33
            }
        return logData

    def __getRegisterMapping__(self):
        datasets = {}
        datasets["power"] = self.__createDataset__(1013, "sum")
        datasets["test"] = self.__createDataset__(1014, "avg")
        datasets["inv"] = self.__createDataset__(1, "avg")
        datasets["temp1"] = self.__createDataset__(1005, "avg")
        return datasets

# Entry Point     
if __name__ == "__main__":

    from mypvdevices.DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    #device connection tests
    serial = "120100200505tes1"
    cryptoKey = "ABABABABABABABAB"
    server = "my-pv.live"

    #AUTO-Tests
    #Constructor Tests
    try:
        device = Device("123456789")
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))
        device = None

    try:
        device = Device(None)
        print(color('ERROR: serial is None.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial is None.', fore='green', style='bright'))

    try:
        device = Device(serial)
        print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
    except:
        print(color('ERROR: creating valid device.', fore='red', style='bright'))

    try:
        setup = device.getSetup()
        if(setup == None):
            raise Exception("Setup is None")
        print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

    try:
        data = device.getData()
        if(data == None):
            raise Exception("Data is None")
        print(color('SUCCESS: getting device data.', fore='green', style='bright'))
    except:
        print(color('ERROR: getting device data.', fore='red', style='bright'))

    try:
        logData = device.getLogData()
        if(logData == None):
            raise Exception("logData is None")
        print(color('SUCCESS: getting device logData.', fore='green', style='bright'))
    except:
        print(color('ERROR: getting device logData.', fore='red', style='bright'))

    try:
        temp = device.getSerial()
        if(temp == serial):
            print(color('SUCCESS: getting device Serial.', fore='green', style='bright'))
        else:
            raise Exception("Serial doesn't match serial used to create.")
    except:
        print(color('ERROR: getting device Serial.', fore='red', style='bright'))

    try:
        device.stop()
        print(color('SUCCESS: stopping device before start.', fore='green', style='bright'))
    except:
        print(color('ERROR: stopping device before start.', fore='red', style='bright'))

    try:
        temp = device.getState()
        if(temp == False):
            print(color('SUCCESS: getting device state (before start).', fore='green', style='bright'))
        else:
            raise Exception("device state is not stopped.")
    except:
        print(color('ERROR: getting device state (before start).', fore='red', style='bright'))

    try:
        temp = device.getDeviceType()
        if(temp == "Dummy-Device"):
            print(color('SUCCESS: getting device type.', fore='green', style='bright'))
        else:
            raise Exception("device type does not match.")
    except:
        print(color('ERROR: getting device type.', fore='red', style='bright'))
  
    if(device != None and not device.setModbusFrequency(None)):
        print(color('SUCCESS: setting modbus frequency (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (None).', fore='red', style='bright'))

    if(device != None and device.setModbusFrequency(0)):
        print(color('SUCCESS: setting modbus frequency (0).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (0).', fore='red', style='bright'))
    
    if(device != None and device.setModbusFrequency(10)):
        print(color('SUCCESS: setting modbus frequency (10).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (10).', fore='red', style='bright'))

    if(device != None and not device.setModbusFrequency(90000)):
        print(color('SUCCESS: setting modbus frequency (90000).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (90000).', fore='red', style='bright'))

    if(device != None and not device.setStartRegister(90000)):
        print(color('SUCCESS: setting modbus startRegister (90000).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (90000).', fore='red', style='bright'))

    if(device != None and device.setStartRegister(1234)):
        print(color('SUCCESS: setting modbus startRegister (1234).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (1234).', fore='red', style='bright'))

    if(device != None and not device.setStartRegister(None)):
        print(color('SUCCESS: setting modbus startRegister (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (None).', fore='red', style='bright'))

    if(device != None and device.setStartRegister(0)):
        print(color('SUCCESS: setting modbus startRegister (0).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (0).', fore='red', style='bright'))

    if(device != None and not device.setRegistersToRead(90000)):
        print(color('SUCCESS: setting modbus registers to read (90000).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (90000).', fore='red', style='bright'))

    if(device != None and not device.setRegistersToRead(None)):
        print(color('SUCCESS: setting modbus registers to read (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (None).', fore='red', style='bright'))

    if(device != None and not device.setRegistersToRead(0)):
        print(color('SUCCESS: setting modbus registers to read (0).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (0).', fore='red', style='bright'))

    if(device != None and device.setRegistersToRead(3)):
        print(color('SUCCESS: setting modbus registers to read (3).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (3).', fore='red', style='bright'))

    key = "ww2target"
    targetValue = 30
    if device != None:
        device.setSetupValue(key, targetValue)
        setup = device.getSetup()
        if(setup[key] == targetValue):
            print(color('SUCCESS: Setting setup value.', fore='green', style='bright'))
        else:
            print(color('ERROR: Setting setup value.', fore='red', style='bright'))

    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        device.addConnection(connection)
        print(color('SUCCESS: adding connection to device.', fore='green', style='bright'))
    except:
        print(color('ERROR: adding connection to device.', fore='red', style='bright'))

    try:
        device.start()
        print(color('SUCCESS: starting device.', fore='green', style='bright'))
    except:
        print(color('ERROR: starting device.', fore='red', style='bright'))

    try:
        temp = device.getState()
        if(temp == True):
            print(color('SUCCESS: getting device state (running).', fore='green', style='bright'))
        else:
            raise Exception("device state is not running.")
    except:
        print(color('ERROR: getting device state (running).', fore='red', style='bright'))

    time.sleep(10)
 
    try:
        device.stop()
        print(color('SUCCESS: stopping device.', fore='green', style='bright'))
    except:
        print(color('ERROR: stopping device.', fore='red', style='bright'))

    try:
        temp = device.getState()
        if(temp == False):
            print(color('SUCCESS: getting device state (stopped).', fore='green', style='bright'))
        else:
            raise Exception("device state is not stopped.")
    except:
        print(color('ERROR: getting device state (stopped).', fore='red', style='bright'))


    device = Device(serial)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addConnection(connection)
    device.start()

    if(device.setLogDataSendInterval(0)):
        print(color('SUCCESS: setting logdata send interval to 0.', fore='green', style='bright'))
    else:
        print(color('ERROR: setting logdata send interval to 0.', fore='red', style='bright'))

    if(device.setLogDataSendInterval(1111111)):
        print(color('ERROR: setting logdata send interval to 1111111.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: setting logdata send interval to 1111111.', fore='green', style='bright'))

    if(device.setLogDataSendInterval(10)):
        print(color('SUCCESS: setting logdata send interval to 10.', fore='green', style='bright'))
    else:
        print(color('ERROR: setting logdata send interval to 10.', fore='red', style='bright'))
    
    time.sleep(20)
 
    #Modbus tests
    device = Device(serial)
    try:
        device.__readRegisters__()
        print(color('SUCCESS: reading registers.', fore='green', style='bright'))
    except:
        print(color('ERROR: reading registers.', fore='red', style='bright'))

    #register change 
    device.__registers__[1022] = 33
    device.__registers__[1023] = 1234
    try:
        device.__syncSettings__()
        if not device.__setup__["ww2target"] == 33:
            raise Exception("ww2target missmatch")
        if not device.__setup__["ww2offset"] == 1514:
            raise Exception("ww2offset missmatch")
        # if not device.__registers__[1023] == 1514:
        #     raise Exception("register 1023 missmatch")
        print(color('SUCCESS: syncing settings.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: syncing settings. ' + str(e), fore='red', style='bright'))
    
    device.__readRegisters__()

    if(device.getRegisterValue(50) == None ):
        print(color('SUCCESS: reading unknown register.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading unknown register.', fore='red', style='bright'))
    
    register = device.getRegisterValue(1014)
    if(register != None and register["value"] == 14000):
        print(color('SUCCESS: reading valid register.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading valid register.', fore='red', style='bright'))

    register = device.getRegisterValue(1003)
    if(register == None):
        print(color('SUCCESS: reading register that should be none.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading register that should be none.', fore='red', style='bright'))

    if(device.getDataset("power") == None ):
        print(color('SUCCESS: getting dataset (power) before processing registers.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (power) before processing registers.', fore='red', style='bright'))

    if(device.getLogValue("power") == None ):
        print(color('SUCCESS: getting logvalue (power) before processing registers.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) before processing registers.', fore='red', style='bright'))

    if(device.getLogValue("test") == None ):
        print(color('SUCCESS: getting logvalue (test) before processing registers.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) before processing registers.', fore='red', style='bright'))

    device.__processRegisters__()

    if(device.getDataset("power") == 1000 ):
        print(color('SUCCESS: getting dataset (power).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (power).', fore='red', style='bright'))

    if(device.getDataset("abc") == None ):
        print(color('SUCCESS: getting dataset (abc).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (abc).', fore='red', style='bright'))

    if(device.getDataset(None) == None ):
        print(color('SUCCESS: getting dataset (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (None).', fore='red', style='bright'))

    if(device.getLogValue(None) == None ):
        print(color('SUCCESS: getting logvalue (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (None).', fore='red', style='bright'))

    if(device.getLogValue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc).', fore='red', style='bright'))

    if( device.getLogValue("power") == 0 ):
        print(color('SUCCESS: getting logvalue (power).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power).', fore='red', style='bright'))

    if( device.getLogValue("test") == 14000 ):
        print(color('SUCCESS: getting logvalue (test).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test).', fore='red', style='bright'))

    time.sleep(1)
    device.__readRegisters__()
    device.__processRegisters__()
    if( device.getLogValue("power") > 0 ):
        print(color('SUCCESS: getting logvalue (power) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after wait.', fore='red', style='bright'))

    if( device.getLogValue("test") == 14000 ):
        print(color('SUCCESS: getting logvalue (test) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after wait.', fore='red', style='bright'))

    if( device.getLogValue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc) after wait.', fore='red', style='bright'))

    device = Device(serial)
    device.__running__ = True
    avgVal0 = device.getLogValue("test")
    sumVal0 = device.getLogValue("power")
    device.__excecuteModbus__()
    avgVal1 = device.getLogValue("test")
    sumVal1 = device.getLogValue("power")
    device.__excecuteModbus__()
    avgVal2 = device.getLogValue("test")
    sumVal2 = device.getLogValue("power")
    device.__excecuteModbus__()
    avgVal3 = device.getLogValue("test")
    sumVal3 = device.getLogValue("power")
    device.__excecuteModbus__()
    avgVal4 = device.getLogValue("test")
    sumVal4 = device.getLogValue("power")
    if( avgVal4 == avgVal1 and sumVal4 > sumVal2):
        print(color('SUCCESS: checking calculation.', fore='green', style='bright'))
    else:
        print(color('ERROR: checking calculation.', fore='red', style='bright'))

    device.clearLog()
    if( device.getLogValue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc) after clear.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc) after clear.', fore='red', style='bright'))

    if( device.getLogValue("test") == None ):
        print(color('SUCCESS: getting logvalue (test) after clear.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after clear.', fore='red', style='bright'))

    if( device.getLogValue("power") == None ):
        print(color('SUCCESS: getting logvalue (power) after clear.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after clear.', fore='red', style='bright'))

    device = Device(serial)
    device.setModbusFrequency(0)
    device.start()
    time.sleep(5)

    if( device.getLogValue("power") == None ):
        print(color('SUCCESS: getting logvalue (power) after starting device with frequency 0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after starting device with frequency 0.', fore='red', style='bright'))
    
    if( device.getLogValue("test") == None ):
        print(color('SUCCESS: getting logvalue (test) after starting device with frequency = 0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after starting device with frequency = 0.', fore='red', style='bright'))

    device.setModbusFrequency(1)
    time.sleep(3)

    if( device.getLogValue("power") > 0 ):
        print(color('SUCCESS: getting logvalue (power) after starting device with frequency >0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after starting device with frequency >0.', fore='red', style='bright'))

    if( device.getLogValue("test") == 14000 ):
        print(color('SUCCESS: getting logvalue (test) after starting device with frequency >0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after starting device with frequency >0.', fore='red', style='bright'))

    device.stop()

    try:
        device.__setHealthState__(0)
        print(color('SUCCESS: setting healthState to 0.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: setting healthState to 0.', fore='red', style='bright'))

    try:
        device.__setHealthState__("seppi")
        print(color('ERROR: setting healthState to invalid.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: setting healthState to invalid.', fore='green', style='bright'))

    try:
        device.__setHealthState__(None)
        print(color('ERROR: setting healthState to None.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: setting healthState to None.', fore='green', style='bright'))

    try:
        device.__setHealthState__(3)
        print(color('SUCCESS: setting healthState to 3.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: setting healthState to 3.', fore='red', style='bright'))

    #DCS communication tests
    device = Device(serial)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addConnection(connection)
    # device.setLogDataSendInterval(5)
    device.start()
    try:
        while True:
            print(color('[Device] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            device.showInfo()
            device.showCommunicationErrors()
            device.showCommunicationErrorsRate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
    input("waiting...")
