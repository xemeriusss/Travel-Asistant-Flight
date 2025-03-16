from langchain.callbacks.base import BaseCallbackHandler

class ToolOutputCatcher(BaseCallbackHandler):
    def __init__(self):

        self.search_flights_outputs = [] # to store search_flights_tool outputs

    def on_tool_end(self, output: str, **kwargs):
        tool_name = kwargs.get("name", "")
        if tool_name == "search_flights_tool":
            self.search_flights_outputs.append(output)

