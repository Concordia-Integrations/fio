#import .interfaces
import time

class TriggerExample():
    _stop = False
    _config = None

    def __init__(self, config):
        self._config = config

    def run(self, queue):
        while not self._stop:
            event = {}
            event["event_field"] = "new event"
            queue.put(event)
            time.sleep(1)

    def stop(self):
        self._stop = True
