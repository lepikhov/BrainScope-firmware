
import time
import bluetooth
from brain_data import BrainData

from config import VREF, CHnSET
from ble_brain import BLEBrain


def get_gain(chan):

    if chan > len(CHnSET):
        return 1.0

    gains = [1.0, 2.0, 4.0, 6.0, 8.0, 12.0, 24.0, 1.0]        
    g = (CHnSET[chan] & 0x70) >> 4
    return gains[g]


sleep = True    

def demo():
    ble = bluetooth.BLE()
    brain = BLEBrain(ble)
    bd = BrainData()
    
    

    def on_rx(v):
        print("RX", v)

    def on_connect():
        bd.wakeup()
        global sleep   
        sleep = False     

    def on_disconnect():
        bd.sleep()   
        global sleep
        sleep = True     

    brain.on_write(on_rx)    

    brain.on_connect(on_connect)    

    brain.on_disconnect(on_disconnect)      

    cnt = 0

    while True:

        time.sleep_ms(1000)         
        
        if sleep:
            continue

        data = [0x1, cnt, 0, 0, 0, 0, 
                0x2, cnt, 0, 0, 0, 0,
                0x3, cnt, 0, 0, 0, 0,
                0x4, cnt, 0, 0, 0, 0,
                0x5, cnt, 0, 0, 0, 0,
                0x6, cnt, 0, 0, 0, 0,
                0x7, cnt, 0, 0, 0, 0,
                0x8, cnt, 0, 0, 0, 0,
                ]
        #tdata = bd.getData()
        tdata = bd.getDataAverage()
        #tdata = bd.getTestData()
        
        for i in range(0, 32, 4):
            u_tmp = int.from_bytes(tdata[i//4], 'little', True)
            s_tmp = u_tmp if u_tmp < (1 << 31) else u_tmp - (1 << 32)
            f_tmp = float(s_tmp)             
            f_tmp *= VREF
            f_tmp /= 8388607.0 # 0x7fffff
            f_tmp /= get_gain(i//4)
            data[2 + i//4 * 6:(i//4 * 6) + 6] = list(int(f_tmp).to_bytes(4, 'little'))
          

        cnt += 1
        try:
            brain.set_data(data, notify=True)
        except:
            print("An exception occurred")

        if not (cnt % 5):
            print(data)



if __name__ == "__main__":
    demo()
