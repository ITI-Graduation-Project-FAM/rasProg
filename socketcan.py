import can

bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=250000)

with bus as bus:
    msg = can.Message(
        arbitration_id=0xAA,
        data=[0, 25, 0, 1, 3, 1, 4, 1],
        is_extended_id=True
    )
    try:
        bus.send(msg)
        print(f"Message sent on {bus.channel_info}")
    except can.CanError:
        print("Message NOT sent")

#for recevung message
    for msg in bus:
        print("ID",msg.arbitration_id,"Data",msg.data)
