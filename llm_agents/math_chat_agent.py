# %pip install "pyautogen[mathchat]~=0.1.1"
import os

import autogen
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent

# config_list = [
#     {
#         'model': 'gpt-4',
#         'api_key': '<your OpenAI API key here>',
#     },
#     {
#         'model': 'gpt-4',
#         'api_key': '<your Azure OpenAI API key here>',
#         'api_base': '<your Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2023-06-01-preview',
#     },
#     {
#         'model': 'gpt-3.5-turbo',
#         'api_key': '<your Azure OpenAI API key here>',
#         'api_base': '<your Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2023-06-01-preview',
#     },
# ]

filter_dict = {
    "api_type": ["open_ai", None],  # None means a missing key is acceptable
    "model": ["gpt-3.5-turbo", "gpt-4"],
}

# Get a list of configs from a json parsed from an env variable or a file.
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict=filter_dict
)

autogen.ChatCompletion.start_logging()

# 1. create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list,
    }
)

# 2. create the MathUserProxyAgent instance named "mathproxyagent"
# By default, the human_input_mode is "NEVER", which means the agent will not ask for human input.
mathproxyagent = MathUserProxyAgent(
    name="mathproxyagent",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)

'''
 Given a math problem, we use the mathproxyagent to generate a prompt to be sent to the assistant as the initial message.
 The assistant receives the message and generates a response. The response will be sent back to the mathproxyagent for processing.
 The conversation continues until the termination condition is met, in MathChat, the termination condition is the detect of "\boxed{}" in the response.
'''

# Example: 1
math_problem = "Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval notation."
mathproxyagent.initiate_chat(assistant, problem=math_problem)

# Example: 2
math_problem = "For what negative value of $k$ is there exactly one solution to the system of equations \\begin{align*}\ny &= 2x^2 + kx + 6 \\\\\ny &= -x + 4?\n\\end{align*}"
mathproxyagent.initiate_chat(assistant, problem=math_problem)

# Example: 3
math_problem = "Find all positive integer values of $c$ such that the equation $x^2-7x+c=0$ only has roots that are real and rational. Express them in decreasing order, separated by commas."
mathproxyagent.initiate_chat(assistant, problem=math_problem)

'''
Check out MathUserProxyAgent.generate_init_message(problem, prompt_type='default', customized_prompt=None):

    You may choose from ['default', 'python', 'two_tools'] for parameter prompt_type. We include two more prompts in 
    the paper: 'python' is a simplified prompt from the default prompt that uses Python only. 'two_tools' further 
    allows the selection of Python or Wolfram Alpha based on this simplified python prompt. Note that this option 
    requries a Wolfram Alpha API key and put it in wolfram.txt. 

    You can also input your customized prompt if needed: mathproxyagent.generate_init_message(problem, customized_prompt="Your customized prompt").
    Since this mathproxyagent detects '\boxed{}' as termination, you need to have a similar termination sentence in the prompt: "If you get the answer, put the answer in \boxed{}.".
    If the customized is provided, the prompt_type will be ignored.
'''

# we set the prompt_type to "python", which is a simplied version of the default prompt.
math_problem = "Problem: If $725x + 727y = 1500$ and $729x+ 731y = 1508$, what is the value of $x - y$ ?"
mathproxyagent.initiate_chat(assistant, problem=math_problem, prompt_type="python")

# The wolfram alpha appid is required for this example (the assistant may choose to query Wolfram Alpha).
# The appid can be obtained from https://www.wolframalpha.com/
# # WOLFRAM_ALPHA_APPID

# we set the prompt_type to "two_tools", which allows the assistant to select wolfram alpha when necessary.
math_problem = "Find all numbers $a$ for which the graph of $y=x^2+a$ and the graph of $y=ax$ intersect. Express your answer in interval notation."
mathproxyagent.initiate_chat(assistant, problem=math_problem, prompt_type="two_tools")