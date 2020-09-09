class TransformExample():
    _config = None

    def __init__(self, config):
        self._config = config

    def transform(self, event):
        event["transformField"] = "enriched the event"
        return event
