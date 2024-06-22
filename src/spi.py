from machine import Pin, SPI

def spi_int():
    hspi = SPI(1, baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=0, 
            sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    CS = Pin(15, Pin.OUT)
    CS.on()

#hspi = SPI(1, SPI.MASTER, baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=0)

 

def spi_transact():
    buf1 = bytearray(1)    
    buf4 = bytearray(4)
    CS.off()
    #hspi.write_readinto(bytes([0x00,0x00,0x00,0x00]),buf4)
    hspi.write_readinto(bytes([0x00]),buf1)
    print("{0:x}".format(buf1[0]))
    CS.on()

            