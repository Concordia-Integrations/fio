import json

class OutputStdout():
    _config = None

    def __init__(self, config):
        _config = config

    def output(self, event):
        json_event = json.dumps(event, indent = 4)
        print(json_event)
