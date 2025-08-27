from langchain_core.tools import BaseTool, StructuredTool, ToolException
from typing import Any
from mcp.types import Tool, CallToolResult, TextContent
from mcp import ClientSession


async def load_converted_tools(session: ClientSession) -> list[BaseTool]:
    tools_result = await session.list_tools()
    tools = tools_result.tools
    return [_convert_mcp_to_langchain_tool(session, tool) for tool in tools]


def _convert_mcp_to_langchain_tool(
        session: ClientSession,
        tool: Tool,
) -> BaseTool:
    async def call_tool(**arguments: dict[str, Any]) -> str | list[str]:
        result = await session.call_tool(tool.name, arguments)
        return _convert_call_tool_result(result)

    return StructuredTool(
        name=tool.name,
        description=tool.description or "",
        args_schema=tool.inputSchema,
        coroutine=call_tool
    )


def _convert_call_tool_result(call_tool_result: CallToolResult) -> str | list[str]:
    if call_tool_result.isError:
        raise ToolException(str(call_tool_result))
    contents = [
        content for content in call_tool_result.content if isinstance(content, TextContent)
    ]
    if len(contents) == 1:
        return contents[0].text
    return [content.text for content in contents]

