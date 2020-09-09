#import pytest
from pipeline import Pipeline
import yaml
import time
import threading

def run_pipeline():
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
    - name: example
      config: {}
    """

    config = yaml.load(yamlConfig, Loader = yaml.SafeLoader)

    pipe = Pipeline(config)

    print("before thread create")

    thread = threading.Thread(target = pipe.run, args=())
    print("before thread start")
    thread.start()
    print("after thread start")
    time.sleep(10)
    print("after 10 seconds")
    pipe.stop()
    thread.join()

run_pipeline()
