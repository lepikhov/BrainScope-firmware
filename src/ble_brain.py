
import bluetooth
from micropython import const

from ble_advertising import advertising_payload


_IRQ_CENTRAL_CONNECT = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT = const(1 << 1)
_IRQ_GATTS_WRITE = const(3)


_BRAIN_SENSE_UUID = bluetooth.UUID('100aae77-d0e8-41bc-81e1-2a6267a79ec5')
_DATA_CHAR = (
    bluetooth.UUID('cdfeec40-9511-11ea-ab12-0800200c9a66'),
    bluetooth.FLAG_NOTIFY,
)

_CONTROL_CHAR = (
    bluetooth.UUID('cdfeec41-9511-11ea-ab12-0800200c9a66'),
    bluetooth.FLAG_WRITE,
)




_BRAIN_SENSE_SERVICES = (
    _BRAIN_SENSE_UUID,
    (_DATA_CHAR, _CONTROL_CHAR),      
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)



class BLEBrain:
    def __init__(self, ble, name="brain_controller", rxbuf=100):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_data, 
          self._handle_control),
        ) = self._ble.gatts_register_services((_BRAIN_SENSE_SERVICES,))
        # Increase the size of the rx buffer and enable append mode.
        #self._ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
        self._connections = set()
        #self._rx_buffer = bytearray()        
        self._write_callback = None

        self._connect_callback = None
        self._disconnect_callback = None

        self._payload = advertising_payload(
            name=name, appearance=_ADV_APPEARANCE_GENERIC_COMPUTER
        )
        self._advertise()

        self._count = 0

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
            if self._connect_callback:
                self._connect_callback()
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            if self._disconnect_callback:
                self._disconnect_callback()
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_control and self._write_callback:
                self._write_callback(value)            

    def set_data(self, data, notify=False):

        if notify:
            for conn_handle in self._connections:
                #pass
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[:6])
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[6:12])
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[12:18])
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[18:24])
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[24:30])               
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[30:36])
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[36:42])
                self._ble.gatts_notify(conn_handle, self._handle_data, bytearray(data)[42:])

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback  

    def on_connect(self, callback):
        self._connect_callback = callback    

    def on_disconnect(self, callback):
        self._disconnect_callback = callback              