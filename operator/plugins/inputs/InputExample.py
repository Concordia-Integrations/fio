class InputExample():
    _config = None

    def __init__(self, config):
        print(config.keys())
        if "eventField" not in config.keys():
            raise Exception("unable to find required input config field eventField")
        self._config = config

    def input(self, event):
        event[self._config["eventField"]] = "input on event"
        return event
