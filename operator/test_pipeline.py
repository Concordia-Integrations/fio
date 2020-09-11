import pytest
from pipeline import Pipeline
import yaml
import time
import threading
from io import StringIO
from unittest.mock import patch

def start_pipeline(yamlConfig):
    config = yaml.load(yamlConfig, Loader = yaml.SafeLoader)
    pipe = Pipeline(config)
    thread = threading.Thread(target = pipe.run, args=())
    thread.start()
    time.sleep(10)
    pipe.stop()
    thread.join()

def test_pipeline():
    #https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-in-python-into-some-sort-of-string-buffer
    print("hello")

    yamlConfig = """
    triggers:
    - name: example
      config: {}
    inputs:
    - name: example
      config:
        eventField: hello
    transforms:
    - name: example
      config: {}
    outputs:
    - name: stdout
      config: {}
    """
    start_pipeline(yamlConfig)

    expected_value = """{
"event_field": "new event",
"hello": "input on event",
"transformField": "enriched the event"
}"""
    with patch('sys.stdout', new = StringIO()) as std_out:
            start_pipeline(yamlConfig)
            assert expected_value in std_out
