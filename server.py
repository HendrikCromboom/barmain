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
    intro = "The available base drinks with their ingredients are as follows:"
    return qa_json_to_tool_str("data", "drinks.json", intro, "drinks", "ingredients")

def qa_json_to_tool_str(directory: str, filename: str, intro: str, question_name: str, answer_name: str ) -> str:
    try:
        path = os.path.join(os.path.dirname(__file__), directory, filename)
        with open(path, "r") as f:
            data = json.load(f)
        string  = intro + "\n\n"
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    question = item.get(question_name, "Unknown " + question_name)
                    answer = item.get(answer_name, "Unknown " + answer_name)
                else:
                    question = f"Item {i}"
                    answer = str(item)

                string += f"Q{i}: {question}\n"
                string += f"A{i}: {answer}\n\n"
        else:
            string += f"Knowledge base content: {json.dumps(data, indent=2)}\n\n"

        return string
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

