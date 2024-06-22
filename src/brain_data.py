import math

from ADS1299x import ADS1299x

from config import CHnSET, VREF



class BrainData:
    def __init__(self):
        self.__countFz=0
        self.__countCz=4
        self.__countOz=8
        self.__countTd=12
        self.__countTs=16

        self.__adc=ADS1299x()

        self.__adc.command(0x06)
        self.__adc.command(0x10)
        self.__adc.command(0x08)

        self.__adc.wreg(0x15, 1, bytearray([0x20]))

        self.__adc.wreg(0x5, 8, bytearray(CHnSET))


    def __point(self, x):
        return int(math.sin(2.0*math.pi*x/32)*0x7fffff)
        

    def getTestData(self):
        data=[int(self.__point(self.__countFz)).to_bytes(4, 'little'),
              int(self.__point(self.__countCz)).to_bytes(4, 'little'),
              int(self.__point(self.__countOz)).to_bytes(4, 'little'),
              int(self.__point(self.__countTd)).to_bytes(4, 'little'),
              int(self.__point(self.__countTs)).to_bytes(4, 'little'),
              int(self.__point(self.__countTs)).to_bytes(4, 'little'),
              int(self.__point(self.__countTs)).to_bytes(4, 'little'),
              int(self.__point(self.__countTs)).to_bytes(4, 'little'),
            ]
        self.__countFz += 1            
        self.__countCz += 1
        self.__countOz += 1
        self.__countTd += 1
        self.__countTs += 1

        return data

    def getData(self):
        data=[]
        buf=self.__adc.getData()
        for i in range(0, 24, 3):
            tmp=int.from_bytes(buf[i:i+3], 'big', True)
            if (tmp&0x800000):  
                tmp |= 0xff000000  
            data.append(int(tmp).to_bytes(4, 'little'))
        return data    
    
    def getDataAverage(self):
        data=[]
        ring_buffers=self.__adc.getBuffers()
        for i in range(8):
            buf=ring_buffers[i].get()
            lng = len(buf)
            if lng:
                tmp = int(sum(buf)/lng)
                if (tmp & 0x800000):  
                    tmp |= 0xff000000               
                data.append(tmp.to_bytes(4, 'little'))
            else:
                data.append(bytearray([0, 0, 0, 0]))                
        return data        

def demo():
    bd=BrainData()
    data=bd.getData()
    #print(data)

if __name__ == "__main__":
    demo()    