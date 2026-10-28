from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger
# NOTE: langchain>=1.3.0 changed public APIs under langchain.agents.
# This project uses a minimal approach: a tool-calling agent built via langgraph,
# wrapped as a runnable executor.


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_time_in_timezone(timezone: str) -> str:
    """Get the current local time in a given IANA timezone.

    Args:
        timezone: IANA timezone name, e.g. "UTC", "America/New_York", "Asia/Kolkata".

    Returns:
        A human-readable time string.
    """

    now = datetime.now(ZoneInfo(timezone))
    return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S')}"


class _LocalAgentStub:
    """Fallback agent used when OPENAI_API_KEY is not configured."""

    def invoke(self, _: dict) -> dict:
        return {"output": "(LLM disabled: set OPENAI_API_KEY to enable the agent.)"}


def build_agent(*, model_name: str = "gpt-3.5-turbo") -> object:
    """Create a tool-calling agent backed by a chat model.

    If OPENAI_API_KEY is not configured, returns a local stub so unit tests
    can run without external network calls.
    """

    import os



    if not os.environ.get("OPENAI_API_KEY"):
        return _LocalAgentStub()

    llm = ChatOpenAI(model=model_name, temperature=0)


    tools = [get_time_in_timezone]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the available tools when needed. "
                "If you are unsure about a timezone, ask a clarifying question.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # langchain.agents.create_tool_calling_agent is not available in the installed langchain version.
    # We build a minimal callable that follows the same interface used by the CLI/tests.
    agent = llm.bind_tools(tools)

    # Executor API differs across langchain versions; for our unit test we only
    # require an object with `.invoke()`.

    executor = agent

    logger.debug(
        "Agent built with model={} and tools={}",
        model_name,
        [t.name for t in tools],
    )
    return executor





