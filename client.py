import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import requests

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

def query(prompt):
    url = "test"
    payload = {
        "model" : "tinyllama",
        "prompt" : prompt,
        "stream" : False
    }
    try: #TODO: Wrap or obfuscate this: Hendrik 24/08/25
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "response" in data:
            return data["response"]
        else:
            raise ValueError("Error")
    except requests.exceptions.ConnectionError:
        return "Could not connect to Ollama. Is it running on the correct port?"

    except requests.exceptions.Timeout:
        return "Request to Ollama timed out. Try increasing the timeout or decrease system load."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"

    except ValueError as val_err:
        return f"Value error: {val_err}"

    except Exception as err:
        return f"An unexpected error occurred: {err}"

if __name__ == "__main__":

    asyncio.run(main())

