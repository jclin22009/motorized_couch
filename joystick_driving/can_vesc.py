from pyvesc import VESC, encode
from pyvesc.VESC.messages import SetRPM

class CanVESC:
    def __init__(self, parent_vesc: VESC, can_id: int):
        self.parent_vesc = parent_vesc
        self.can_id = can_id

    def set_rpm(self, rpm: int):
        packet = encode(SetRPM(rpm,can_id=self.can_id))
        self.parent_vesc.write(packet)

    def get_rpm(self):
        # TODO
        return 1000

    def stop_heartbeat(self):
        # Make sure to stop the hearbeat of the parent VESC
        return