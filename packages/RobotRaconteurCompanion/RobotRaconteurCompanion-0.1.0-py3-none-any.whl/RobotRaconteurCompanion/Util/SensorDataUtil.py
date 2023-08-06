import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import numpy as np

from .DateTimeUtil import DateTimeUtil

class SensorDataUtil(object):

    def __init__(self, node = None, client_obj = None):
        if node is None:
            self._node = RRN
        else:
            self._node = node
        self._client_obj = client_obj

        self._sensordataheader = node.GetStructureType("com.robotraconteur.sensordata.SensorDataHeader", self._client_obj)
        
        self._datetime_util = DateTimeUtil(node,client_obj)

    def FillSensorDataHeader(self, device_info, seqno):
        ret = self._sensordataheader()
        ret.seqno = seqno
        ret.ts = self._datetime_util.TimeSpec2Now(device_info)
        return ret

