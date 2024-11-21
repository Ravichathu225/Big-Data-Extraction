from agency_swarm import Agent
from .tools.getbigdata_tool import DBreaderTool

class readbigdata(Agent):
    def __init__(self):
        super().__init__(
            name="Big Data Analyzer Agent",
            description="Analyzes and read Database get finance report",
            instructions="./instructions.md",
            tools=[DBreaderTool],
            temperature=0.5,
            max_prompt_tokens=25000,
        )
        