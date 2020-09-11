#TODO: made imports dynamic

from plugins.triggers import TriggerExample
from plugins.inputs import InputExample
from plugins.transforms import TransformExample
from plugins.outputs import OutputExample
from plugins.outputs import OutputStdout
import queue
import importlib
import threading
import time

class Pipeline():
    _queue = queue.Queue()
    _pipeline_config = None

    _triggers = []
    _inputs = []
    _transforms = []
    _outputs = []
    _stop = False
    _trigger_threads = []

    def __init__(self, pipeline_config):
        self._pipeline_config = pipeline_config
        self._register_plugin("trigger", self._triggers)
        self._register_plugin("input", self._inputs)
        self._register_plugin("transform", self._transforms)
        self._register_plugin("output", self._outputs)

    def _register_plugin(self, plugin_type, plugin_list):
        for plugin in self._pipeline_config[plugin_type + "s"]:
            class_name = plugin_type.capitalize() + plugin["name"].capitalize()
            module_name = "plugins." + plugin_type + "s"
            plugins_module = importlib.import_module(module_name)
            module = getattr(plugins_module, class_name)
            klass = getattr(module, class_name)
            instance = klass(plugin["config"])
            plugin_list.append(instance)

    def _run_tick(self):
        while not self._queue.empty():
            event = self._queue.get(block=False)

            for input in self._inputs:
                event = input.input(event)

            for transform in self._transforms:
                event = transform.transform(event)

            for output in self._outputs:
                output.output(event)

    def run(self):
        for trigger in self._triggers:
                thread = threading.Thread(target = trigger.run, args=(self._queue,))
                print("before trigger start")
                thread.setDaemon(True)
                thread.start()
                print("after trigger start")
        while not self._stop:
            time.sleep(1)
            self._run_tick()


    def stop(self):
        for trigger in self._triggers:
            trigger.stop()
        self._stop = True
