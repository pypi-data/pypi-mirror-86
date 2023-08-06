#!/usr/bin/python

import logging
from datetime import datetime, timedelta
import time
import socket
import random
import json
import threading
import queue
import string
from xtea import MODE_CBC, new
from colr import color

JOINTIMEOUT = 3
RECEIVEMQSITZE = 10
SERIALLEN = 16
CRYPTOKEYLEN = 16
ACKTIMEOUT = 3
BUFFERSIZE = 2048
SOCKETRETRIES = 3
SOCKETWAITTIME = 1
KEEPALIVEFREQUENCY = 30
RECONNECTTIMEOUT = 5

class DcsConnection:
    __serial__ = None
    __cryptoKey__ = None
    __serverAddress__ = None
    __serverPort__ = None
    __socket__ = None
    __connected__ = False
    __receiveBuffer__ = None
    __receiverThread__ = None
    __workerThread__ = None
    __socketLock__ = None
    __threadLock__ = None
    __messageLock__ = None
    __running__ = False
    __sentRequests__ = None
    __ackReceivedEvent__ = None
    __receivedMessageQueue__ = None
    __lastMessageTime__ = None
    __lastMessageSendTime__ = None
    __keepConnected__ = False
    __device__ = None
    __logData__ = None
    
    def __init__(self, serial, cryptoKey, server, port):
        if serial != None and len(serial) == SERIALLEN:
            self.__serial__ = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)

        if cryptoKey != None and len(cryptoKey) == CRYPTOKEYLEN and type(cryptoKey) == str:
            self.__cryptoKey__ = cryptoKey.encode('utf-8')
        else:
            errmsg = "Instance not created. CryptoKey invalid. CryptoKey=" + str(cryptoKey)
            logging.error(errmsg)
            raise ValueError(errmsg)

        if server != None:
            self.__serverAddress__ = server
        else:
            errmsg = "Instance not created. Server is required"
            logging.error(errmsg)
            raise ValueError(errmsg)
        
        if port != None and port > 0 and port < 65636:
            self.__serverPort__ = port
        else:
            errmsg = "Instance not created. Port out of range. Port=" + str(port)
            logging.error(errmsg)
            raise ValueError(errmsg)

        self.__socketLock__ = threading.Lock()
        self.__threadLock__ = threading.Lock()
        self.__messageLock__ = threading.Lock()
        self.__sentRequests__ = dict()
        self.__ackReceivedEvent__ = threading.Event()
        self.__receivedMessageQueue__ = queue.Queue(RECEIVEMQSITZE)

        logging.debug("DcsConnection created. Serial: " + str(self.__serial__))

    def __del__(self):
        self.__running__ = False

    def getServer(self):
        return self.__serverAddress__

    def getSocketHash(self):
        return self.__socket__.__hash__()

    def addDevice(self, device):
        if(device != None):
            self.__device__ = device
            return True
        else:
            return False

    def isConnected(self):
        return self.__connected__

    def connect(self):
        logging.info(str(id(self)) + " connecting " + str(self.__serial__ ) + "@" + str(self.__serverAddress__) + ":" + str(self.__serverPort__) + "...")
        if(self.__connected__ == True):
            return True

        self.__lastMessageTime__ = None
        if(not self.__running__):
            self.__start__()
        else:
            logging.debug(str(id(self)) + " threads already running")
        result = self.__dcsConnect__()
        self.__keepConnected__ = True
        return result

    def disconnect(self):
        self.__keepConnected__ = False
        self.__connected__ = False
        self.__stop__()
        result = self.__dcsDisconnect__()
        if(result):
            logging.info(str(id(self)) + " successfully disconnected")
        else:
            logging.warning(str(id(self)) + "cannont disconnect")
        return result
        
    def reconnect(self):
        self.__connected__ = False
        self.__keepConnected__ = False
        result = self.__dcsDisconnect__()
        if(result):
            logging.info(str(id(self)) + " successfully disconnected. Ready to reconnect")
        else:
            logging.warning(str(id(self)) + "cannont disconnect")
        return self.connect()

    def __createReceiverThread__(self):
        return threading.Thread(target=self.__receive__, name="DCS-RECEIVER "+str(self.__serial__ )+"@"+str(self.__serverAddress__)+":"+str(self.__serverPort__))

    def __createWorkerThread__(self):
        return threading.Thread(target=self.__worker__, name="DCS-WORKER "+str(self.__serial__ )+"@"+str(self.__serverAddress__)+":"+str(self.__serverPort__))

    def __start__(self):
        logging.debug("Threads starting...")
        self.__running__ = True
        self.__receiverThread__ = self.__createReceiverThread__()
        self.__workerThread__ = self.__createWorkerThread__()
        try:
            self.__receiverThread__.start()
            self.__workerThread__.start()
        except Exception as e:
            logging.warning("Threads starting with Exception " + str(e))
    
    def __stop__(self):
        logging.debug("Threads stopping...")
        self.__connected__ = False
        self.__threadLock__.acquire()
        self.__running__ = False
        self.__threadLock__.release()
        if(self.__receiverThread__ != None and self.__receiverThread__.is_alive()):
            self.__receiverThread__.join(JOINTIMEOUT)
        logging.debug("Receiver stopped. ")
        if(self.__workerThread__ != None and self.__workerThread__.is_alive()):
            self.__workerThread__.join(JOINTIMEOUT)
        logging.debug("Worker stopped.")

    ##receiving messages
    def __receive__(self):
        logging.debug(str(id(self)) + " Receiver running...")
        while self.__running__ == True:
            wait = False
            self.__socketLock__.acquire()
            if(self.__socket__ != None and not self.__socket__._closed):
                try:
                    rec = self.__socket__.recv(BUFFERSIZE)
                    self.__receiveBuffer__ += rec
                except BlockingIOError as e:
                    if e.errno != 10035 and e.errno != 11:
                        logging.error(str(id(self)) + " BlockingIOError: " + str(e))
                except Exception as e:
                    logging.error(str(id(self)) + " Unknown error receiving data from socket. " + str(e))
                    wait = True
            self.__socketLock__.release()

            if(wait == True):
                wait = False
                time.sleep(SOCKETWAITTIME)

            if self.__receiveBuffer__ != None and len(self.__receiveBuffer__)>=32:			
                rec_serialno = self.__receiveBuffer__[0:SERIALLEN].decode("utf-8")
                rec_tid = int.from_bytes(self.__receiveBuffer__[SERIALLEN:18],"little")
                rec_msgtype = int(self.__receiveBuffer__[18])
                rec_paylen = int.from_bytes(self.__receiveBuffer__[19:21],"little")
                rec_payload = self.__receiveBuffer__[32:(32+rec_paylen)]
                self.__receiveBuffer__ = self.__receiveBuffer__[(32+rec_paylen):]

                if(rec_serialno != self.__serial__ ):
                    logging.warning(str(id(self)) + " Invalid serial in received data: " + str(rec_serialno))
                else:
                    logging.debug(str(id(self)) + " Received TID:" + str(rec_tid) + "; Type:" + str(rec_msgtype) + " Paylen: "+str(rec_paylen))
                    message = {
                        "tid": rec_tid,
                        "type": rec_msgtype,
                        "payload": rec_payload
                    }
                    self.__receivedMessageQueue__.put(message)
                    self.__lastMessageTime__ = datetime.now()

    #handling massages
    def __worker__(self):
        logging.debug(str(id(self)) + " Worker running...")
        while self.__running__ == True:
            message = None         
            try:
                message = self.__receivedMessageQueue__.get_nowait()
            except:
                pass

            if(message):
                logging.debug(str(id(self)) + " Handling Message: " + str(message))
                try:
                    self.__handleMessage__(message["type"], message["payload"], message["tid"])
                except Exception as e:
                    logging.error(str(id(self)) + " Error handling message. " + str(e))

    def __handleMessage__(self, msgType, payload, tid):
        if(msgType == 9):
            logging.debug(str(id(self)) + " TID: " + str(tid) + "; Received ACK")
            try:
                self.__ackRequest__(tid)    #just notify waiting messages and do nothing more
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error handling ACK")
            return

        if(msgType == 8):
            logging.debug(str(id(self)) + " TID: " + str(tid) + "; Received Keep Alive.")
            try:
                self.__send__(None, 9, tid, isResponce=True)     #send ACK
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending ACK")
            return

        if(msgType == 4):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Received Curent Data Request.")
            try:
                self.sendData(tid=tid)
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending data." +  str(e))
            return

        if(msgType == 5):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Received Setup Change.")
            try:
                self.__changeSetup__(payload)
            except Exception as e:
                logging.error(str(id(self)) + " Error applying setup changes. " + str(e))
            try:
                self.sendSetup(tid=tid)
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending setup response")
            return

        if(msgType == 6):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Calc Log Daten (für MSG.Type 2).")
            try:
                self.loadLogData()
            except Exception as e:
                logging.warning(str(id(self)) + " TID: " + str(tid) + "; Error getting logData")
            try:
                self.__send__(None, 9, tid, isResponce=True)     #send ACK
                self.clearLogData()
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending ACK for Calc Log Data")
            return

        if(msgType == 7):
            logging.info(str(id(self)) + " TID: " + str(tid) + "; Send Log Daten (MSG.Type 2).")
            try:
                self.sendLogData(tid=tid)
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + "; Error sending logData.")
            return

        logging.info(str(id(self)) + " TID: " + str(tid) + "; Unknown MSG-Type received: " + str(msgType) + ".")
    
    def watchdog(self):
        logging.debug(str(id(self)) + " Watchdog running...")
        self.__threadLock__.acquire()
        if(self.__running__ != True):
            self.__threadLock__.release()
            return

        if(self.__receiverThread__ != None and not self.__receiverThread__.is_alive()):
            logging.warning(str(id(self)) + " Receiver thread death. Restarting...")
            try:
                self.__receiverThread__ = self.__createReceiverThread__()
                self.__receiverThread__.start()
            except Exception as e:
                logging.warning(str(id(self)) + " Error restarting receiver Thread: " + str(e))
        
        if(self.__workerThread__ != None and not self.__workerThread__.is_alive()):
            logging.warning(str(id(self)) + " Worker thread death. Restarting...")
            try:
                self.__workerThread__ = self.__createWorkerThread__()
                self.__workerThread__.start()
            except Exception as e:
                logging.warning(str(id(self)) + " Error restarting worker Thread: " + str(e))
        self.__threadLock__.release()
        
        if(self.__lastMessageTime__ != None):
            difference = datetime.now() - self.__lastMessageTime__
            if(difference.total_seconds() > KEEPALIVEFREQUENCY):
                logging.error(str(id(self)) + " No message received for more then " + str(KEEPALIVEFREQUENCY) + " secunds. Reconnecting...")
                try:
                    self.reconnect()
                except Exception as e:
                    logging.warning(str(id(self)) + "Cannot reconect. " + str(e))

        if(self.__keepConnected__ == True and self.__connected__ != True):
            logging.error(str(id(self)) + " disconnection detected. Reconnecting...")
            try:
                self.reconnect()
            except Exception as e:
                logging.warning(str(id(self)) + "Cannot reconect. " + str(e))
        logging.debug(str(id(self)) + " MSQ-Size: " + str(self.__receivedMessageQueue__.qsize()))

    def __cleanSentrequests__(self):
        cleanList = []
        for request in self.__sentRequests__:
            try:
                if self.__sentRequests__[request] != None and self.__sentRequests__[request]["timestamp"] < datetime.now() - timedelta(seconds=90):
                    cleanList.append(request)
            except Exception as e:
                logging.debug(str(id(self)) + " request " + str(request) + " element does not exist anymore. " + str(e))

        for element in cleanList:
            try:
                logging.debug(str(id(self)) + " Cleaning up request " + str(element) + ".")
                del self.__sentRequests__[element]
            except Exception as e:
                logging.debug(str(id(self)) + " Cannot clean request " + str(element) + ". " + str(e))

    def __dcsConnect__(self):
        if not self.__connected__:
            self.__sentRequests__.clear()
            logging.debug(str(id(self)) + " preparing socket.... ")
            if(self.__checkSocket__()):
                try:
                    self.sendSetup(True)
                except Exception as e:
                    logging.error(str(id(self)) + " connection failed. " + str(e))
                    return False

                self.__connected__ = True
                logging.debug(str(id(self)) + " connected " + str(self.__serial__ ))
                return True
            else:
                logging.error(str(id(self)) + " connection failed. No socket available")
                return False

    def __checkSocket__(self):
        self.__socketLock__.acquire()
        result = True
        if self.__socket__ == None or self.__socket__._closed:
            result = self.__openSocket__()
        self.__socketLock__.release()
        return result

    def __openSocket__(self):
        socketRetries = 0
        logging.debug(str(id(self)) + " No socket. Opening socket...")
        self.__socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket__.settimeout(RECONNECTTIMEOUT)
        self.__receiveBuffer__ = bytes()
        host = ""
        try:
            host = socket.gethostbyname(self.__serverAddress__)
        except:
            logging.error(str(id(self)) + " Host not found.")
            self.__socket__ = None
            return False

        while(socketRetries <= SOCKETRETRIES):
            try:
                logging.debug(str(id(self)) + " trying to connect socket " + str(host) + ":" + str(self.__serverPort__) + "...")
                self.__socket__.connect((host, self.__serverPort__))
                break
            except:
                logging.warning(str(id(self)) + " Cannot connect to " + str(host) + ":" + str(self.__serverPort__) + ".")
                socketRetries = socketRetries + 1
                time.sleep(SOCKETWAITTIME)
            if socketRetries > SOCKETRETRIES:
                self.__socket__ = None
                
        if(self.__socket__ != None):
            self.__socket__.setblocking(0)
            return True
       
        logging.info(str(id(self)) + " Opening socket failed. Too many retries: " + str(socketRetries))
        return False

    def __dcsDisconnect__(self):
        if self.__socket__ == None or self.__socket__._closed:
            logging.info(str(id(self)) + " Socket is already closed")
            return True
        try:
            self.__closeSocket__()
            logging.info(str(id(self)) + " Socket closed")
            return True
        except Exception as e:
            logging.error(str(id(self)) + " closing socket failed. " + str(e))
            return False

    def __closeSocket__(self):
        self.__socketLock__.acquire()
        self.__socket__.close()
        self.__socketLock__.release()

    def __ackRequest__(self, tid):
        self.__messageLock__.acquire()
        try:
            self.__sentRequests__[tid]["state"] = "ACK"
            self.__sentRequests__[tid]["timestamp"] = datetime.now()
        except Exception as e:
            logging.warning(str(id(self)) + " TID: " + str(tid) + " Request not found. ACK not set. " + str(e))

        try:
            self.__sentRequests__[tid]["event"].set()
        except Exception as e:
            logging.warning(str(id(self)) + " TID: " + str(tid) + " Request not found. Could not wakeup. " + str(e))
        self.__messageLock__.release()

    def __send__(self, payload, msgtype, tid, isResponce=False, nack=False):
        if self.__socket__ == None or self.__socket__._closed:
            errmsg = str(id(self)) + "Cannot send. No open Socket."
            logging.error(errmsg)
            raise ConnectionError(errmsg)
        try:
            package = self.__make_package__(self.__serial__ , payload, msgtype, tid, nack)
        except Exception as e:
            return False
        if package != None:
            if self.__registerMessage__(tid, msgtype):
                try:
                    self.__socketLock__.acquire()
                    self.__socket__.send(package)
                    # self.__socket__.sendall(package)
                    self.__lastMessageSendTime__ = datetime.now()
                    logging.debug(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " transmitted.")
                    self.__socketLock__.release()
                except Exception as e:
                    logging.error(str(id(self)) + " cannot send. " + str(e))
                    self.__socketLock__.release()
                    return False
                
                if(isResponce == False):
                    if(not self.__waitForAck__(tid)): 
                        logging.warning(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " no ACK received.")
                        return False
                logging.debug(str(id(self)) + " TID: " + str(tid) + "; Type: " + str(msgtype) + " successfull send.")
                return True
            else:
                return False
        else:
            logging.error(str(id(self)) + " no package to send")
            return False

    def __registerMessage__(self, tid, msgType):
        if msgType == 9:
            return True;
        self.__messageLock__.acquire()
        self.__cleanSentrequests__()
        try:
            self.__sentRequests__[tid]
            if self.__sentRequests__[tid] != None:
                logging.error("[" + self.__serial__ + "] tid " + str(tid) + " already in use")
                self.__messageLock__.release()
                return False
        except:
            pass

        event = threading.Event()
        self.__sentRequests__[tid] = {
            "timestamp": datetime.now(),
            "event": event,
            "state": "NEW"
        }
        self.__messageLock__.release()
        return True

    def __waitForAck__(self, tid):
        self.__messageLock__.acquire()
        try:
            if(self.__sentRequests__[tid]["state"] != "ACK"):
                self.__sentRequests__[tid]["state"] = "SEND"
                self.__sentRequests__[tid]["timestamp"] = datetime.now()
                event = self.__sentRequests__[tid]["event"]
            else:
                event = None
        except Exception as e:
            logging.warning(str(id(self)) + " TID: " + str(tid) + " MSG not registrated. " + str(e))
            self.__messageLock__.release()
            return False
        self.__messageLock__.release()

        if(event):
            event.wait(ACKTIMEOUT)

        response = False
        self.__messageLock__.acquire()
        try:
            if(self.__sentRequests__[tid]["state"] == "ACK"):
                response = True
            del self.__sentRequests__[tid]
        except Exception as e:
            logging.warning(str(id(self)) + " TID: " + str(tid) + " MSG not found. " + str(e))
        self.__messageLock__.release()
        return response

    def __wakeUpWaitingMessages__(self):
        self.__socketLock__.acquire()
        for item in self.__sentRequests__.values():
            temp = item["event"]
            temp.set()
        self.__socketLock__.release()

    def __make_package__(self, device_serno, payl, msgtype, tid, nack=False):
        if(len(device_serno) != SERIALLEN):
            errorMsg = str(id(self)) + " invalid serial " + str(device_serno)
            logging.warning("TID: " + str(tid) + " MakePackage: " + str(errorMsg))
            raise Exception(errorMsg)

        if(msgtype == None):
            errorMsg = str(id(self)) + " no MSGTYPE set "
            logging.warning("TID: " + str(tid) + " MakePackage: " + str(errorMsg))
            raise Exception(errorMsg)

        if(tid == None):
            errorMsg = str(id(self)) + " invalid TID " + str(tid)
            logging.warning("TID: " + str(tid) + " MakePackage: " + str(errorMsg))
            raise Exception(errorMsg)

        if(payl != None):
            try:
                payload = json.dumps(payl).encode('utf-8')
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + " Invalid Payload: " + str(payl) + ". " + str(e))
                return False
        else:
            payload = bytes()
        
        try:
            rand = self.__get_random_string__(8)
            iv = rand.encode('utf-8')
        except Exception as e:
            logging.error("TID: " + str(tid) + " Error generating IV: " + str(e))
            raise(e)
        xtea = new(self.__cryptoKey__, mode = MODE_CBC, IV = iv)

        missing = 8 - len(payload) % 8
        if missing < 8:
            payload = payload + B'\x00' * missing   #always multiple of 8
        if(len(payload) != 0):
            payload = random.randint(0, 2^32).to_bytes(4, byteorder="little")+random.randint(0, 2^32).to_bytes(4, byteorder="little") + payload      # add 8 bytes for initial vector
       
        payload = xtea.encrypt(payload)
        payloadLengh = len(payload).to_bytes(2, byteorder="little")    #calc payload
        Cloudsocket_tid= tid.to_bytes(2, byteorder="little")
        Cloudsocket_msgtype = bytes([msgtype])
        if nack == True:
            ackn = B'\x00'
        else:
            ackn = B'\x01'
        if self.__device__ != None:
            try:
                healthState = self.__device__.getHealthState()
            except Exception as e:
                logging.error("TID: " + str(tid) + " Cannot get healthstate: " + str(e))
                healthState = 0
        else:
            healthState = 0
        healthStateByte = healthState.to_bytes(1, byteorder="little")
        header = device_serno.encode('utf-8') + Cloudsocket_tid + Cloudsocket_msgtype + payloadLengh + ackn + healthStateByte + B'\x00'*9  #build 32 byte header
        package = header + payload
        return  package

    def __get_random_string__(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str 

    def __decryptPayload__(self, payload):
        xtea = new(self.__cryptoKey__, mode=MODE_CBC,IV=payload[32:40])
        payload_decrypted = xtea.decrypt(payload)[8:]
        payload_string = payload_decrypted.decode()
        message_string = payload_string[payload_string.find("?")+1:]
        setup_string = message_string[0:message_string.find("/")]
        logging.debug("["+str(self.__serial__ )+"@"+str(self.__serverAddress__)+":"+str(self.__serverPort__)+"]; Setup changes: " + str(setup_string))
        elements = setup_string.split("&")
        return elements

    def sendData(self, tid=None):
        if(self.__connected__):
            data = self.__getCurrentData__()
            if(tid == None):
                isResponce=False
                tid = self.__getTid__()
            else:
                isResponce=True
                if(tid > 65535 or tid < 1):
                    raise Exception("TID out of range (1-65535)")
            logging.info(str(id(self)) + " TID: " + str(tid) + ", sending data: " + str(data))
            try:
                if(not self.__send__(data, 1, tid, isResponce=isResponce)):
                    raise Exception("Cannot send data. TID: " + str(tid) + ". " + str(data))
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + ", Error: " + str(e))
                raise
        else:
            errormsg = str(id(self)) + " Error sendig Data. Not connected"
            logging.error(errormsg)
            raise Exception(errormsg)

    def sendLogData(self, tid=None):
        logData = self.__logData__
        if(logData == None):
            error = str(id(self)) + " Cannot send logData. Empty Logdata."
            logging.warning(error)
            raise Exception(error)

        if(self.__connected__):
            if(tid == None):
                tid = self.__getTid__()
                isResponce = False
            else:
                isResponce = True
                if(tid > 65535 or tid < 1):
                    raise Exception("TID out of range (1-65535)")
            logging.info(str(id(self)) + " TID: " + str(tid) + ", sending logData: " + str(self.__logData__))
            try:
                if(not self.__send__(logData, 2, tid, isResponce=isResponce)):
                    raise Exception("Error sending logData.")
            except Exception as e:
                logging.error(str(id(self)) + " TID: " + str(tid) + ", Error: " + str(e))
                raise
        else:
            errormsg = "Error sendig LogData. Not connected"
            logging.error(errormsg)
            raise Exception(errormsg)

    def __getTid__(self):
        self.__messageLock__.acquire()
        found = None
        while found == None:
            tid = random.randint(1, 65535)
            try:
                self.__sentRequests__[tid]
            except:
                found = tid
                self.__sentRequests__[tid] = None
        self.__messageLock__.release()
        return found

    def sendSetup(self, forced = None, tid=None):
        if(self.__connected__ or forced):
            setup = self.__getSetup__()
            if(tid == None):
                tid = self.__getTid__()
                isResponce = False
            else:
                isResponce = True
                if(tid > 65535 or tid < 1):
                    raise Exception("TID out of range (1-65535)")
            logging.info(str(id(self)) + " TID: " + str(tid) + ", sending setup: " + str(setup))
            try:
                if(not self.__send__(setup, 3, tid, isResponce=isResponce)):
                    raise Exception("Error sending setup.")
            except Exception as e:
                logging.error("TID: " + str(tid) + ", Error: " + str(e)) 
                raise
        else:
            errormsg = "Error sendig Setup. Not connected"
            logging.error(errormsg)
            raise Exception(errormsg)

    def __getSetup__(self):
        if(self.__device__ == None):
            logging.warning(str(id(self)) + " device not found. sending dummy setup")
            return {"device": "ConnectionTest", "fwversion": "1.0.0", "serialno": self.__serial__ }
        else:
            return self.__device__.getSetup()

    def __getCurrentData__(self):
        if(self.__device__ == None):
            logging.warning(str(id(self)) + " device not found. getting dummy currData")
            t = datetime.now()
            return {"power": t.second * 100}
        else:
            return self.__device__.getData()
    
    def loadLogData(self):
        if(self.__device__ == None):
            logging.warning(str(id(self)) + " device not found. getting dummy logData")
            t = datetime.now()
            self.__logData__ = {"i_power": t.second * 100}
        else:
            self.__logData__ = self.__device__.getLogData()

    def clearLogData(self):
        if(self.__device__ == None):
            logging.warning(str(id(self)) + " device not found. nothing to clean.")
        else:
            self.__device__.clearLog()

    def __changeSetup__(self, payload):
        try:
            setupChanges = self.__decryptPayload__(payload)
            logging.debug(str(id(self)) + " Changing setup: " + str(setupChanges))
        except Exception as e:
            error = str(id(self)) + " Error decoding setup changes: " + str(e)
            logging.error(error)
            setupChanges = None
            raise Exception(error)

        if(setupChanges != None):
            for elements in setupChanges:
                setting = elements.split("=")
                field = setting[0]
                value = int(setting[1])

                if(self.__device__ == None):
                    logging.warning(str(id(self)) + " device not found. Settings not applied.")
                    print("Field:" + str(field) + "; Value=" + str(value))
                else:
                    self.__device__.setSetupValue(field, value)        					

# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    serial = "120100200505tes1"
    serial2 = "120100200505tes2"
    serial3 = "120100200505tes3"
    cryptoKey = "ABABABABABABABAB"
    cryptoKeyInvalid = "ABABABABABABAB00"
    server = "my-pv.live"

    #AUTO-Tests
    #Constructor Tests
    try:
        DcsConnection("toShort", cryptoKey, server, 50333)
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))

    try:
        DcsConnection(serial, cryptoKey, server, None)
        print(color('ERROR: Creation without port.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without port.', fore='green', style='bright'))

    try:
        DcsConnection(serial, cryptoKey, server, 123456789)
        print(color('ERROR: Creation invalid port.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation invalid port.', fore='green', style='bright'))

    try:
        DcsConnection(serial, cryptoKey, None, 50333)
        print(color('ERROR: Creation without server.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without server.', fore='green', style='bright'))

    try:
        DcsConnection(serial, None, server, 50333)
        print(color('ERROR: Creation without CryptoKey.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without CryptoKey.', fore='green', style='bright'))

    try:
        DcsConnection(serial, "tooShortKey", server, 50333)
        print(color('ERROR: Creation with to short CryptoKey.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation with to short CryptoKey.', fore='green', style='bright'))

    try:
        DcsConnection(None, cryptoKey, server, 50333)
        print(color('ERROR: Creation without serial.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: Creation without serial.', fore='green', style='bright'))

# Connection Tests
    #connecting to unknown host
    connection = DcsConnection(serial, cryptoKey, "noserver.my-pv.live", 50333)
    if(connection.connect()):
        print(color('ERROR: Connecting to invalid host.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting to invalid host.', fore='green', style='bright'))
    connection.disconnect()
    
    #connecting to invalid port
    connection = DcsConnection(serial, cryptoKey, server, 1234)
    if(connection.connect()):
        print(color('ERROR: Connecting to invalid port.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting to invalid port.', fore='green', style='bright'))
    connection.disconnect()

    #regular connection
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    if(not connection.connect()):
        print(color('ERROR: Regular connection.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Regular connection.', fore='green', style='bright'))
    connection.disconnect()

    if(not connection.disconnect()):
        print(color('ERROR: disconnection.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: disconnection.', fore='green', style='bright'))
    connection.disconnect()

    #reconnecting
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    if(not connection.reconnect()):
        print(color('ERROR: reconnection.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: reconnection.', fore='green', style='bright'))
    connection.disconnect()

    #connecting to twice
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    if(not connection.connect()):
        print(color('ERROR: Connecting twice.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting twice.', fore='green', style='bright'))
    connection.disconnect()

    #connecting after disconnecting
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    connection.disconnect()
    if(not connection.connect()):
        print(color('ERROR: Connecting again.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connecting again.', fore='green', style='bright'))
    connection.disconnect()

    #connecting with invalid cryptoKey
    connection = DcsConnection(serial, "1111111111111111", server, 50333)
    if(connection.connect()):
        print(color('ERROR: Connection with an invalid crypto key esteblished.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connection with an invalid crypto key failed.', fore='green', style='bright'))
    try:
        connection.sendData()
        print(color('ERROR: sending data with invalid encryption Key.', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: sending data with invalid encryption Key.', fore='green', style='bright'))
    connection.disconnect()

    #connecting unknown device
    connection = DcsConnection("0123456789ABCEFG", cryptoKey, server, 50333)
    if(connection.connect()):
        print(color('ERROR: Connection using an unknown serial esteblished.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Connection using an unknown serial failed.', fore='green', style='bright'))
    try:
        connection.sendData()
        print(color('ERROR: sending data with unknown device.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending data with unknown device.', fore='green', style='bright'))
    connection.disconnect()

    #Starting/Stopping Thread
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        connection.__start__()
        time.sleep(2)
        connection.__stop__()
        print(color('SUCCESS: Starting/Stopping Thread.', fore='green', style='bright'))
    except Exception as e:
        print(e)
        print(color('ERROR: Starting/Stopping Thread.', fore='red', style='bright'))
    connection.disconnect()

    #sending using valid connection after trying to connect with an invalid connection
    #valid connection
    connection = DcsConnection(serial, cryptoKey, server, 50333) 
    state = connection.connect()
    #connection with invalid key but same serial
    connection2 = DcsConnection(serial, cryptoKeyInvalid, server, 50333) 
    state2 = connection.connect()
    #send data using first valid connection
    try:
        connection.sendData()
        print(color('SUCCESS: sending using valid connection after trying to connect with an invalid connection.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending using valid connection after trying to connect with an invalid connection.', fore='red', style='bright'))
    connection.disconnect()
    connection2.disconnect()

#Communication Tests
    #send without beeing connected
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        connection.sendSetup()
        print(color('ERROR: sending setup without beeing connected.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending setup without beeing connected.', fore='green', style='bright'))

    try:
        connection.sendData()
        print(color('ERROR: sending data without beeing connected.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending data without beeing connected.', fore='green', style='bright'))

    try:
        connection.loadLogData()
        connection.clearLogData()
        connection.sendLogData()
        print(color('ERROR: sending logData without beeing connected.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: sending logData without beeing connected.', fore='green', style='bright'))

    try:
        connection.connect()
    except Exception as e:
        print(color('ERROR: Cannot connect for connection tests.', fore='red', style='bright'))

    try:
        connection.sendData()
        print(color('SUCCESS: sending data.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending data.', fore='red', style='bright'))

    try:
        connection.loadLogData()
        connection.clearLogData()
        connection.sendLogData()
        print(color('SUCCESS: sending logData.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending logData.', fore='red', style='bright'))

    try:
        connection.sendSetup()
        print(color('SUCCESS: sending setup.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending setup.', fore='red', style='bright'))

    connection.disconnect()

    #sending empty logData
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    try:
        connection.sendLogData()
        print(color('ERROR: sending empty logData.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: sending empty logData.', fore='green', style='bright'))
    connection.disconnect()

    ##active/passive clients tests
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection.connect()
    socketHash = connection.getSocketHash()
    time.sleep(15 + KEEPALIVEFREQUENCY)
    if(connection.isConnected() and socketHash == connection.getSocketHash()):
        print(color('SUCCESS: Check isConnected.', fore='green', style='bright'))
    else:
        print(color('ERROR: Check isConnected.', fore='red', style='bright'))

    #switch to active client by sending data
    try:
        connection.loadLogData()
        connection.clearLogData()
        connection.sendLogData()
        print(color('SUCCESS: sending unexpected logData after waiting.', fore='green', style='bright'))
    except:
        print(color('ERROR: sending unexpected logData after waiting.', fore='red', style='bright'))
    #switch to active client by sending data   
    try:
        connection.sendData()
        print(color('SUCCESS: sending unexpected currData after waiting.', fore='green', style='bright'))
    except:
        print(color('ERROR: sending unexpected currData after waiting.', fore='red', style='bright'))
    
    time.sleep(10 + KEEPALIVEFREQUENCY)
    if(connection.isConnected() and socketHash == connection.getSocketHash()):
        print(color('SUCCESS: Check if socket has changed.', fore='green', style='bright'))
    else:
        print(color('ERROR: Check if socket has changed. Old socket-Hash: ' + str(socketHash) + ', new socket-Hash: ' + str(connection.getSocketHash()), fore='red', style='bright'))
    connection.disconnect()

    ## watchdog tests
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        connection.watchdog()
        print(color('SUCCESS: Watchdog without started connection.', fore='green', style='bright'))
    except:
        print(color('ERROR: Watchdog without started connection.', fore='red', style='bright'))
    connection.connect()
    try:
        connection.watchdog()
        print(color('SUCCESS: Watchdog with started connection.', fore='green', style='bright'))
    except:
        print(color('ERROR: Watchdog with started connection.', fore='red', style='bright'))
    connection.disconnect()

    input(color('[DCS-Connection] AUTO-Tests finished. Press enter to continue...', fore='blue', style='bright'))

    connection = DcsConnection(serial, cryptoKey, server, 50333)
    connection2 = DcsConnection(serial2, cryptoKey, server, 50333)
    connection3 = DcsConnection(serial3, cryptoKey, server, 50333)
    connection.connect()
    connection2.connect()
    connection3.connect()
    hash1 = connection.getSocketHash()
    hash2 = connection2.getSocketHash()
    hash3 = connection3.getSocketHash()
    try:
        while True:
            print(color('[DCS-Connection] Communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            connection.watchdog()
            connection2.watchdog()
            connection3.watchdog()
            if(hash1 != connection.getSocketHash()):
                print(color('[DCS-Connection] Socket of serial ' + str(serial) + ' has changed.', fore='red', style='bright'))
                hash1 = connection.getSocketHash()
            if(hash2 != connection2.getSocketHash()):
                print(color('[DCS-Connection] Socket of serial ' + str(serial2) + ' has changed.', fore='red', style='bright'))
                hash2 = connection2.getSocketHash()
            if(hash3 != connection3.getSocketHash()):
                print(color('[DCS-Connection] Socket of serial ' + str(serial3) + ' has changed.', fore='red', style='bright'))
                hash3 = connection3.getSocketHash()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        connection.disconnect()
        connection2.disconnect()
        connection3.disconnect()

    time.sleep(1)
    # input(color('[DCS-Connection] Press enter to exit...', fore='blue', style='bright'))
