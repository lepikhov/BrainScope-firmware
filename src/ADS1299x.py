from machine import Pin, SPI, enable_irq, disable_irq
from ring_buffer import RingBuffer
from config import RING_BUFFER_SIZE


class ADS1299x:

    WAKEUP = 0x02
    STANDBY = 0x04
    RESET = 0x06
    START = 0x08
    STOP = 0x0A
    RDATAC = 0x10



    def __init__(self):
        self.__hspi = SPI(1, baudrate=5000000, polarity=0, phase=1, bits=8, firstbit=SPI.MSB, 
            sck=Pin(14), mosi=Pin(13), miso=Pin(12))
        self.__hspi.init()    
        self.__CS = Pin(15, Pin.OUT)
        self.__CS.on()

        self.__buf = bytearray(27)

        self.__DATAREADY = Pin(27, Pin.IN, Pin.PULL_UP)
        self.__DATAREADY.irq(trigger=Pin.IRQ_FALLING, handler=self.__DR_callback)

        self.__ring_buffers = [
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
            RingBuffer(RING_BUFFER_SIZE),
        ]


    def __DR_callback(self, pin):
        
        self.__CS.off()
        self.__buf=self.__hspi.read(27)
        self.__CS.on()

        buf = bytearray(24)
        buf=self.__buf[3:] 
        for i in range(0, 24, 3):
            tmp=int.from_bytes(buf[i:i+3], 'big', True) 
            self.__ring_buffers[i//3].append(tmp)

    def command(self, cmnd):
        buf = bytearray(1)
        buf[0] = cmnd

        self.__CS.off()
        self.__hspi.write(buf)
        self.__CS.on()

    def wreg(self, reg, num, data):
        buf = bytearray(2)
        buf[0] = 0x40+(reg & 0x1f)
        buf[1] = (num-1) & 0x1f  
        
        self.__CS.off()
        self.__hspi.write(buf)
        self.__hspi.write(data)
        self.__CS.on()


    def getData(self):
        buf = bytearray(32)
        state=disable_irq()
        buf=self.__buf[3:]         
        enable_irq(state)

        return buf
    
    def getBuffers(self):
        return self.__ring_buffers