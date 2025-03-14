# callback.py
from langchain.callbacks.base import BaseCallbackHandler

class ToolOutputCatcher(BaseCallbackHandler):
    """
    A callback to catch the outputs from any tool the agent calls.
    If the tool is "search_flights_tool", we store its output for later use.
    """
    def __init__(self):
        self.search_flights_output = None

    def on_tool_end(self, output: str, **kwargs):
        # This is called whenever any tool finishes execution.
        tool_name = kwargs.get("name", "")
        if tool_name == "search_flights_tool":
            # Store the raw output from the flight search tool
            self.search_flights_output = output
