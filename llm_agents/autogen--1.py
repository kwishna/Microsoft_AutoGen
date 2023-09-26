from autogen import AssistantAgent, UserProxyAgent
assistant = AssistantAgent("assistant")
user_proxy = UserProxyAgent("user_proxy")
user_proxy.initiate_chat(assistant, message="Plot a chart of META and TESLA stock price change YTD.")
# This initiates an automated chat between the two agents to solve the task