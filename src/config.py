VREF=4500000.0 #mkV
RING_BUFFER_SIZE=50


#CHnSET=[0x60, 0x60, 0x40, 0x40, 0x00, 0x00, 0x61, 0x61]
#CHnSET=[0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01] # all closed, GAIN = 1
#CHnSET=[0x61, 0x61, 0x61, 0x61, 0x61, 0x61, 0x61, 0x61] # all closed, GAIN = 24
CHnSET=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # all open, GAIN = 1
#CHnSET=[0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60] # all open, GAIN = 24
#CHnSET=[0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x00] # all open, GAIN = 1, 2, 4, 6, 8, 12, 24, 1