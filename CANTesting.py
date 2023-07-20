import CanModule
import threading
import can
import time
def hello(var=can.Message):
    print("hello")
    print(var.data)



#bus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=250000)
# fun=hello()
#can.Notifier(bus=bus,listeners=[hello])
myvar=CanModule.CANOBJ()
myvar.addListener(Callable= hello)
#time.sleep(3)
#myvar.stopLiseners()