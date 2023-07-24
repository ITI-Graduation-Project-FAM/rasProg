import can 

def send1(arbitration_id=0x124,data=0x1,is_Extended_id=False):
        busv = can.interface.Bus(interface='socketcan', channel='can0', bitrate=400000)
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=is_Extended_id,
        )
        try:
            busv.send(msg)
            # print(f"Message sent on {busv.channel_info}")
            busv.shutdown()
        except can.CanError:
            print("Message NOT sent") 