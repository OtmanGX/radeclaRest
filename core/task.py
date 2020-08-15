import re
import time
from threading import Thread, Lock
# from core.models import Reservation
import serial
from django.utils import timezone
SERIAL_PORT = '/dev/ttyACM0'

lock = Lock()


class ReservationMsg:
    regex = re.compile(r"^[01];[01];\d;[12];$")
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
        self.msg = None
        SerialThread.begin = True

    def send(self, msg, msg2):
        lock.acquire()
        if self.ser is not None:
            print('sending', msg)
            print('sending', msg2)
            self.ser.write(msg)
            time.sleep(4)
            self.ser.write(msg2)
        lock.release()

    def run(self):
        while True:
            try:
                # time.sleep(1)
                if self.ser is None:
                    self.ser = serial.Serial(SERIAL_PORT, 9600, timeout=2)
                    print('link serial')
                    # time.sleep(2)
                if self.ser is not None:
                    if self.msg is not None :
                        self.send(self.msg[0], self.msg[1])
                        self.msg = None
                    else:
                        tram = self.ser.readline().decode().strip()
                        if len(tram):
                            print('received', tram)
                            t = ReservationMsg(tram)
                            if t is not None:
                                from core.models import Reservation
                                # print(t)
                                now = timezone.now()
                                try:
                                    time.sleep(6)
                                    res = Reservation.objects.get(terrain=1, start_date__hour=t.content[2] + 6,
                                                              start_date__day=now.day, start_date__month=now.month, start_date__year=now.year)
                                    # res.eclairage_paye =
                                    res.eclairage_paye = t.content[3] == 1
                                    res.eclairage = t.content[3] == 1
                                    print(res.eclairage)
                                    res.save()
                                except Exception as e:
                                    print(e)
            except Exception as e:
                self.ser = None
                print('exception', e)
                time.sleep(1)
