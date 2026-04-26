import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core import tools

load_dotenv()

import openlit

openlit.init(
    otlp_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://alloy:4318"),
    application_name=os.getenv("OPENLIT_APPLICATION_NAME", "langchain-demo"),
    environment=os.getenv("OPENLIT_ENVIRONMENT", "development"),
)


@tools.tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tools.tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def main(query):
    llm = init_chat_model("claude-opus-4-7", model_provider="anthropic")
    llm_tools = [add, multiply]
    llm_with_tools = llm.bind_tools(llm_tools)

    messages = [HumanMessage(query)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    response = llm_with_tools.invoke(messages)
    print(response.content)
    return response.content


if __name__ == "__main__":
    import time
    query = "What is 3 * 12? Also, what is 11 + 49?"
    while True:
        main(query)
        time.sleep(20)
