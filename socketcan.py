import can

#make this file as class and call it in main file
class CanModule:
    def __init__(self,filters=None):
        if filters is None:
            filters = [
                {"can_id": 0x10, "can_mask": 0x10, "extended": False},
                {"can_id": 0x2, "can_mask": 0x2, "extended": False},
            ]
        self.bus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=250000,can_filters=filters)
    def send(self,arbitration_id,data,is_Extended_id=False):
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=True
        )
        try:
            self.bus.send(msg)
            print(f"Message sent on {self.bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")
    def receive(self):
        for msg in self.bus:
            print("ID",hex(msg.arbitration_id),"Data",msg.data)



