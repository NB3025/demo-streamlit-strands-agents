from strands import Agent, tool
from strands_tools import file_read
from strands.models import BedrockModel
import logging

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.DEBUG)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", 
    handlers=[logging.StreamHandler()]
)

model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
bedrock_model = BedrockModel(max_tokens=4096, model_id=model_id)

system_prompt = """
당신은 Agent입니다. 사용자의 질문에 답하세요. 
사용자가 정비 항목에 대한 질문을 하면 search_vehicle_maintenance을 사용하세요.
"""

# agent = Agent(model=bedrock_model, system_prompt=system_prompt, 
#               tools=[])

# response = agent("엔진오일 정비 기간 알고 싶어")


class MyAgent():

    def __init__(self):
        self.agent = Agent(model=bedrock_model, system_prompt=system_prompt, tools=[])
    
    def get_agent(self):
        return self.agent



