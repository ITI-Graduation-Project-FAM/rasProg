import can
import time
#make this file as class and call it in main file
class CANOBJ(object):
    ST1HEXsendID=0x100
    Notifier=None
    answer=0
    # zero state indcates that the app is not running
    # one state indcates that the app is running in ST opreating mode
    # two state indcates that the app is running in ST bootloader mode
    # three state indcates that the app is running in ST bootloader mode and the hex file is being sent
    ST1currentstate=0
    ST2currentstate=0
    st1requestedstate=1
    st2requestedstate=1
    def __init__(self,filters=None):
        if filters is None:
            filters = [
                {"can_id": 0x10  , "extended": False},#for firmware version number from ST1
                {"can_id": 0x11  , "extended": False},#for Temp reading from st1  to raspberry
                {"can_id": 0x12  , "extended": False},#for current reading from ST1 to raspberry
                {"can_id": 0x13  , "extended": False},#for Voltage reading from ST1 to raspberry
                {"can_id": 0x14  , "extended": False},#for PWM reading from ST2 to raspberry pi
                {"can_id": 0x15  , "extended": False},#for firmware version number from ST2 to raspberry
                {"can_id": 0x16  , "extended": False},#for Start Sending Firmware Hex to ST1 from rasp
                {"can_id": 0x17  , "extended": False},#for Start Sending Firmware Hex to ST2 from rasp
                {"can_id": 0x18  , "extended": False},#for Sending PWM Value to ST2 from rasp--onhold
                {"can_id": 0x19  , "extended": False},#for start signal from ST1 to raspberry 
                {"can_id": 0x20  , "extended": False},#for start signal from ST2 to raspberry
                {"can_id": 0x21  , "extended": False},#for start app signal to ST2 from raspberry
                {"can_id": 0x22  , "extended": False},#for start app signal to ST1 from raspberry
                {"can_id": 0x23  , "extended": False},#for hex file record to st1
                {"can_id": 0x24  , "extended": False},#for hex file record to st2
                {"can_id": 0x25  , "extended": False},#for hex file newline to st2
                {"can_id": 0x26  , "extended": False},#for hex file newline to st1
                {"can_id": 0x27  , "extended": False},#for signal from st1 ready to receive hex file
                {"can_id": 0x28  , "extended": False},#for signal from st2 ready to receive hex file
                {"can_id": 0x29  , "extended": False},#for signal from st1 ready to receive next line
                {"can_id": 0x30  , "extended": False},#for signal from st2 ready to receive next line
                {"can_id": 0x31  , "extended": False},##for end of hex file transmission to st1
                {"can_id": 0x32  , "extended": False},#for end of hex file transmission to st2
                {"can_id": 0x33  , "extended": False},#for signal from raspberry to st1 to stop app and start bootloader(restart)
                {"can_id": 0x34  , "extended": False},#for signal from raspberry to st2 to stop app and start bootloader(restart)
                {"can_id": 0x35  , "extended": False},#for signal from raspberry to st1 to start app to st1 --onhold
                {"can_id": 0x36  , "extended": False},#for signal from raspberry to st2 to start app to st2 --onhold
                {"can_id": 0x37  , "extended": False},#for Temp reading from st1  to st2
                {"can_id": 0x38  , "extended": False},#for current  reading from ST1 to ST2
                {"can_id": 0x39  , "extended": False},#for Voltage reading from ST1 to ST2
                {"can_id": 0x40  , "extended": False},#for motor speed from st1 to st2

            ]
        self.bus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=400000)
        
    
    def addListener(self,Callable):
        self.Notifier=can.Notifier(bus=self.bus,listeners=[Callable])

    def stopLiseners(self,Callable):
        self.Notifier.remove_listener([Callable])
           

    def send(self,arbitration_id,data,is_Extended_id=False):
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=is_Extended_id
        )
        try:
            self.bus.send(msg)
            # print(f"Message sent on {self.bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")
    
    def receive(self):
        for msg in self.bus:
            print("ID",hex(msg.arbitration_id),"Data",msg.data)
    

            
    def send_hexFileCAN(self,passedfile='file.hex',stnumber=1):
        # modify the IDs of messages according to the ST number
        if(stnumber==1):
            StartHexID=0x16
            HexRecordID=0x23
            HexnewLineID=0x26
        elif(stnumber==2):
            StartHexID=0x17
            HexRecordID=0x24
            HexnewLineID=0x25
        global answer
        # global bus
        self.addListener(busp=self.bus,Callable= self.handleincoming)
        len=0
        dataarray=""
        filelocation=0
        recordlocation=0
        currentrecordAdd=""
        currentrecordType=""
        isEndOfFile=False
        # send the signal of start sending hex file
        self.send(StartHexID,0x1,False)

        with open(passedfile, 'r') as file:
            wholevalue = file.read()
            for value in wholevalue:
                answer=0
                if(value==':'):
                    continue
                filelocation+=1
                len+=1
                dataarray+=value
                recordlocation+=1
                # store the current record address
                if(recordlocation>=3 and recordlocation<=6):
                    currentrecordAdd+=value
                # check if the record is end of line

                if(recordlocation>=7 and recordlocation<=8):
                    currentrecordType+=value
                
                #check if the record is end of file
                if(currentrecordType=="01"):
                    isEndOfFile=True
                if(value =='\n'):
                    # print((bytes.fromhex(dataarray)).hex(),end="")
                    self.send(HexRecordID,(bytes.fromhex(dataarray)),False)
                    self.waitingforanswer(printdelay=0.00001)
                    print("Record  ",currentrecordAdd,"sent")
                    self.send(HexnewLineID,0x1,False)
                    self.waitingforanswer(printdelay=0.00001)
                    if(isEndOfFile):
                        print("End of file")
                        print("Firmware sent successfully")
                        self.stopLiseners(Callable= self.handleincoming)
                        return 0
                    dataarray=""
                    len=0
                    recordlocation=0
                    currentrecordType=""
                    currentrecordAdd=""
                elif(len==16):
                    # print((bytes.fromhex(dataarray)).hex(),end="")
                    self.send(HexRecordID,(bytes.fromhex(dataarray)),False)
                    dataarray=""
                    len=0
                    answerstate=self.waitingforanswer(printdelay=0.00001)
                    if(answerstate==1):
                        print("Error in sending hex file")
                        self.stopLiseners(Callable= self.handleincoming)
                        return 1
                    else:
                        continue
                

    def waitingforanswer(self,printdelay=0.01):
        global answer
        # wait for answer from st1 for 5 seconds
        for i in range(500000):
            if(answer==0):
                time.sleep(printdelay)
                continue
            elif(answer==1):
                answer=0
                return 0
        print("No answer received")
        return 1
                
                
    
    def handleincoming(var=can.Message):
        global answer
        # print("ID ", var.arbitration_id,"DATA",var.data)
        # send(bus,0x124,0x1,False)
        if(var.arbitration_id==0x23):
            pass
        elif(var.arbitration_id==0x29):
            # print("answer received")
            # wriefile('\n',False)
            answer=1
