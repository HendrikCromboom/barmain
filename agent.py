from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import ToolMessage, BaseMessage, SystemMessage, HumanMessage
from langchain_core.messages.tool import ToolCall
from langchain_core.tools import BaseTool

SYSTEM_PROMPT = """
You are a personal bar assistant responsible for cocktail and drink suggestions and providing
recipes for cocktails and drinks
<instructions>
    <instruction> Always use the tools that are provided for suggesting drinks and their respective recipes</instruction>
    <instruction> The get_drinks tool will return a list of drinks, from this list you can suggest the most matching cocktail and its ingredients</instruction>
    <instruction> Only use one tool call per user query</instruction>
    <instruction> Never duplicate tool calls</instructions>
</instructions>

Your responses have to be in human language, much like a butler would speak.
""".strip()


def create_history() -> list[BaseMessage]:
    return [SystemMessage(content=SYSTEM_PROMPT)]


async def call_tool(tool_call: ToolCall, all_tools: list[BaseTool]) -> ToolMessage:
    tool_call_id = tool_call["id"]
    all_tools_by_name = {tool.name: tool for tool in all_tools}
    tool = all_tools_by_name[tool_call["name"]]
    response = await tool.ainvoke(tool_call["args"])
    return ToolMessage(content=str(response), tool_call_id=tool_call_id)


async def ask(
        query: str,
        history: list[BaseMessage],
        llm: BaseChatModel,
        tools: list[BaseTool],
        max_iterations: int,
) -> str:
    n_iterations = 0
    messages = history.copy()
    messages.append(HumanMessage(content=query))

    while n_iterations < max_iterations:
        response = await llm.ainvoke(messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content
        for tool_call in response.tool_calls:
            response = await call_tool(tool_call, tools)
            messages.append(response)
        n_iterations += 1

    raise RuntimeError(
        "Max iterations: Something might be wrong with the prompt"
    )
