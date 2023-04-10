from can2RNET import Can2RNET

# create a Can2RNET instance
can_bus = Can2RNET()

# define the CAN message ID and data for driving forward
msg_id = 0x601
msg_data = [0x02, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00]

# send the CAN message
can_bus.send_message(msg_id, msg_data)