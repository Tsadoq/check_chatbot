from typing import List

from dotenv import load_dotenv, find_dotenv
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.tools import Tool
from haystack_experimental.components.agents import Agent

from agents.prompts import prompt_check_mk_agent

load_dotenv(find_dotenv())

def return_check_mk_helper_agent(tool_list: List[Tool]) -> Agent:
    """
    Return the CheckMK Helper Agent
    :param tool_list: List[Tool], the list of tools to be used by the agent
    :return: Agent, the CheckMK Helper Agent
    """
    checkmk_helper_agent = Agent(
        chat_generator=OpenAIChatGenerator(model="gpt-4o"),
        system_prompt=prompt_check_mk_agent,
        tools=tool_list,
        exit_condition="text",
    )

    return checkmk_helper_agent