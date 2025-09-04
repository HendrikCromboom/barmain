import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from tool_adapter import load_converted_tools
from agent import ask, create_history
from langchain_ollama import ChatOllama
from fastapi import FastAPI

app = FastAPI()


@app.post("/generate")
async def generate(prompt: str):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            response = await query(prompt, create_history(), ChatOllama(model="llama3.2:1b"), session)
            return {"response": response}


async def main_man():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("BarmAIn is thinking... This might take a minute...")
            print(
                await query("What are the ingredients for a mojito?", create_history(), ChatOllama(model="llama3.2:1b"),
                            session))


async def query(prompt: str, history: list, llm, session: ClientSession) -> str:
    tools = await load_converted_tools(session=session)
    llm_tooled = llm.bind_tools(tools)
    return await ask(prompt, history, llm_tooled, tools, 10)
