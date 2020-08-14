import re
import time
from threading import Thread
# from core.models import Reservation
import serial
from django.utils import timezone
SERIAL_PORT = '/dev/ttyACM0'

class ReservationMsg:
    regex = re.compile(r"[01];[01];\d;[01];")
    lastValue = 0

    def __new__(cls, tram):
        if cls.regex.search(tram) is None:
            return None
        else:
            return super().__new__(cls)

    def __init__(self, msg):
        try:
            self.content = list(map(int, msg.rstrip(';').split(';')))
        except Exception as e:
            print(e)


class SerialThread(Thread):
    begin = False

    def __init__(self):
        super().__init__(name="serialThread")
        print('Thread created')
        self.ser = None
        self.count = 0
        SerialThread.begin = True

    def send(self, msg):
        if self.ser:
            self.ser.write(msg)

    def run(self):
        while True:
            # try:
            if self.ser is None:
                self.ser = serial.Serial(SERIAL_PORT, 9600, timeout=2)
                time.sleep(2)
            if self.ser is not None:
                tram = self.ser.readline().decode().strip()
                print(tram)
                t = ReservationMsg(tram)
                if t is not None:
                    from core.models import Reservation
                    print(t)
                    now = timezone.now()
                    res = Reservation.objects.get(terrain=1, start_date__hour=t.content[2] + 6,
                                                  start_date__day=now.day, start_date__month=now.month, start_date__year=now.year)
                    # res.eclairage_paye =
                    res.eclairage = bool(t.content[3])
                    res.save()
            # except Exception as e:
            #     self.ser = None
            #     print('exception', e)
            #     time.sleep(1)
