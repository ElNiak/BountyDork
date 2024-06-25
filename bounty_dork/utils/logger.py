# Setup logging
from datetime import datetime
import sys
import threading

today_date = datetime.now()
orig_stdout = sys.stderr
f = open(f'outputs/logs/"{today_date}".log', "w")
lock_stderr = threading.Lock()


class Unbuffered:
    def __init__(self, stream):
        self.stream = stream

    def flush(self):
        pass

    def write(self, data):
        with lock_stderr:
            self.stream.write(data)
            f.write(data)  # Write the data of stdout here to a text file as well
            # self.stream.flush()
            # f.flush()


sys.stderr = Unbuffered(sys.stderr)
