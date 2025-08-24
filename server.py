from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import json

load_dotenv()

runtime_env = os.getenv('RUNTIME_ENV')

mcp = FastMCP(
    name = "barmAIn",
    stateless_http = True
)
@mcp.tool()
def something(example: str) -> str:
    return example + " something something"
@mcp.tool()
def get_drinks() -> str: #TODO: Wrap or obfuscate
    try:
        path = os.path.join(os.path.dirname(__file__), "data", "drinks.json")
        with open(path, "r") as f:
            data = json.load(f)
        drinks = "The available base drinks with their ingredients are as follows:\n\n"
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    question = item.get("question", "Unknown question")
                    answer = item.get("answer", "Unknown answer")
                else:
                    question = f"Item {i}"
                    answer = str(item)

                drinks += f"Q{i}: {question}\n"
                drinks += f"A{i}: {answer}\n\n"
        else:
            drinks += f"Knowledge base content: {json.dumps(data, indent=2)}\n\n"

        return drinks
    except FileNotFoundError:
        return "Error: Knowledge base file not found"
    except json.JSONDecodeError:
        return "Error: Invalid JSON in knowledge base file"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":

    if runtime_env == "test":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif runtime_env == "docker":
        print("Running Local MCP Server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown env: {runtime_env}")

