import struct
from app.constant import MESSAGETYPES_SLAVES


def convert_payload(payload, type):
    if type not in MESSAGETYPES_SLAVES:
        return None

    # Temp and Hum
    if type == MESSAGETYPES_SLAVES[0]:
        result = dict()

        try:
            result["temp"] = struct.unpack("f", payload[0:4])[0]
            result["hum"] = struct.unpack("f", payload[4:8])[0]
        except:
            return None

        return result
