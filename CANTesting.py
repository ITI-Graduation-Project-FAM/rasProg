import CanModule
import threading
import can
import time
import sendonly as sendonly
global answer
answer=0

def hello(var=can.Message):
    print("hello")
    print(var.data)

def handleincoming(var=can.Message):
    global answer
    global bus
    # print("ID ", var.arbitration_id,"DATA",var.data)
    # send(bus,0x124,0x1,False)
    if(var.arbitration_id==0x23):
        pass
        #print(var.data.hex())
        # wriefile(var.data.hex(),False)
    elif(var.arbitration_id==0x29):
        # print("answer received")
        # wriefile('\n',False)
        answer=1

def wriefile(data, ishex=False):
    with open("receivedFile.hex","a") as receivedfile:
        if(ishex):
            receivedfile.write(data.hex())
            print(data.hex(),end="")
        else:
            receivedfile.write(data)
            print(data,end="")
        #    receivedfile.write(data.hex())
        #    receivedfile.close()

def send_hexFile2(passedfile='file.hex'):
    len=0
    dataarray=""
    filelocation=0
    with open(passedfile, 'r') as file:
        wholevalue = file.read()
        for value in wholevalue:
            if(value==':'):
                 continue
            filelocation+=1
            len+=1
            dataarray+=value
            #wrie a code to print hi every 16 char
            if(value =='\n'):
                # print((bytes.fromhex(dataarray)).hex(),end="")
                wriefile((bytes.fromhex(dataarray)),True)
                wriefile('\n',False)
                dataarray=""
                len=0
            elif(len==16):
                # print((bytes.fromhex(dataarray)).hex(),end="")
                wriefile((bytes.fromhex(dataarray)),True)
                dataarray=""
                len=0

def send_hexFileCAN(passedfile='file.hex'):
    global answer
    global bus
    bus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=400000)
    addListener(busp=bus,Callable= handleincoming)
    len=0
    dataarray=""
    filelocation=0
    recordlocation=0
    currentrecordAdd=""
    currentrecordType=""
    isEndOfFile=False
    sendonly.send1(0x16,0x1,False)
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
                sendonly.send1(0x23,(bytes.fromhex(dataarray)),False)
                waitingforanswer(printdelay=0.00001)
                print("Record  ",currentrecordAdd,"sent")
                sendonly.send1(0x26,0x1,False)
                waitingforanswer(printdelay=0.00001)
                if(isEndOfFile):
                    print("End of file")
                    print("Firmware sent successfully")
                    break
                dataarray=""
                len=0
                recordlocation=0
                currentrecordType=""
                currentrecordAdd=""
            elif(len==16):
                # print((bytes.fromhex(dataarray)).hex(),end="")
                sendonly.send1(0x23,(bytes.fromhex(dataarray)),False)
                dataarray=""
                len=0
                waitingforanswer(printdelay=0.00001)
            




def addListener(busp,Callable):
        can.Notifier(bus=busp,listeners=[Callable])
def waitingforanswer(printdelay=0.01):
    global answer
    while(answer==0):
        # print("answer is",answer)
        # time.sleep(0.01)
        # print("waiting for answer")
        time.sleep(printdelay)
        continue
    answer=0
    # print("answer is",answer)
    # print("answer received")
    return 1


#send_hexFileCAN('stmf103_blinkDebugPins.hex')
send_hexFileCAN('ADC_LM35.hex')
#send_hexFileCAN('CAN_New.hex')


#testing sending file 

# bus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=250000)
# fun=hello()
#can.Notifier(bus=bus,listeners=[hello])
#myvar=CanModule.CANOBJ()
#myvar.addListener(Callable= hello)
#time.sleep(3)
#myvar.stopLiseners()