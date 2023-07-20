import can

#make this file as class and call it in main file
class CANOBJ(object):
    ST1HEXsendID=0x100
    Notifier=None
    def __init__(self,filters=None):
        if filters is None:
            filters = [
                {"can_id": 0x10 , "can_mask": 0x7ff  , "extended": False},#for firmware version number from ST1
                {"can_id": 0x11  , "can_mask": 0x7ff  , "extended": False},#for Temp reading from st1
                {"can_id": 0x12  , "can_mask": 0x7ff  , "extended": False},#for current reading from ST1
                {"can_id": 0x13  , "can_mask": 0x7ff  , "extended": False},#for Voltage reading from ST1
                {"can_id": 0x14  , "can_mask": 0x7ff  , "extended": False},#for PWM reading from ST2
                {"can_id": 0x15 , "can_mask": 0x7ff  , "extended": False},#for firmware version number from ST1

            ]
        self.bus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=250000)
        

    def addListener(self,Callable):
        self.Notifier=can.Notifier(bus=self.bus,listeners=[Callable])

    def stopLiseners(self):
        self.Notifier.stop()
           

    def send(self,arbitration_id,data,is_Extended_id=False):
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=is_Extended_id
        )
        try:
            self.bus.send(msg)
            print(f"Message sent on {self.bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")
    
    def receive(self):
        for msg in self.bus:
            print("ID",hex(msg.arbitration_id),"Data",msg.data)
    
    def send_hexFile(self):
        with open('file.hex', 'r') as file:
            hex_lines = file.readlines()
            
            # Send the hex file in batches of 1 lines
            for i in range(0, len(hex_lines), 1):
                batch_lines = hex_lines[i:i+1]
            
                # Create the data to send
                data = []
                for line in batch_lines:
                    # Convert each line to bytes and append to the data list
                    line_data = bytes.fromhex(line.strip())
                    data.extend(line_data)
            
                # Send the data using the CAN module
                self.send(self.ST1HEXsendID, data, is_Extended_id=False)
            
                # Wait for "OK" response before sending the next batch
                response = None
                while response is None or response.data != b'OK':
                    response = self.receive()
            
                print("Received OK response")
            
            


