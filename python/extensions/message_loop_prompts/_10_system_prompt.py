from datetime import datetime
from python.helpers.extension import Extension
from agent import Agent, LoopData
from copy import deepcopy


class SystemPrompt(Extension):

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        # append main system prompt and tools
        main = get_main_prompt(self.agent)
        tools = get_tools_prompt(self.agent)
        loop_data.system.append(main)
        loop_data.system.append(tools)

        # add dynamic variables to the last message in conversation
        if loop_data.history:
            loop_data.history = list(loop_data.history) # shallow copy of the list
            last_message = deepcopy(loop_data.history[-1]) # deep copy of the last message

            # prepare dynamic info
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            agent_name = self.agent.agent_name
            dynamic_info = f"\n\nSYSTEM INFO: Current time is {date_time}. Your name is {agent_name}."

            # append to content
            if hasattr(last_message, 'content'):
                last_message.content += dynamic_info
                loop_data.history[-1] = last_message

def get_main_prompt(agent: Agent):
    return get_prompt("agent.system.main.md", agent)

def get_tools_prompt(agent: Agent):
    return get_prompt("agent.system.tools.md", agent)

def get_prompt(file: str, agent: Agent):
    return agent.read_prompt(file)
