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
    response = requests.post(url, payload)
    return response.json()["response"]

if __name__ == "__main__":

    asyncio.run(main())

