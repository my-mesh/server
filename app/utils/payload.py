import struct
from constant import MESSAGETYPES_SLAVES

def convert_payload(payload, type):
    if type not in MESSAGETYPES_SLAVES:
        return None
    
    # Temp and Hum
    if type == MESSAGETYPES_SLAVES[0]:
        temp = None
        hum = None

        try:
            temp = struct.unpack("f", payload[0:4])
            hum = struct.unpack("f", payload[4:8])
        except:
            return None
        
        return {
            "temp": temp[0],
            "hum": hum[0]
        }