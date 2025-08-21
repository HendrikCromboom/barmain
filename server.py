from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv()

runtime_env = os.getenv('RUNTIME_ENV')

mcp = FastMCP(
    name = "barmAIn",
    stateless_http = True
)
@mcp.tool()
def something(example: str) -> str:
    return example + " something something"

if __name__ == "__main__":

    if runtime_env == "test":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif runtime_env == "docker":
        print("Running Local MCP Server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown env: {runtime_env}")

