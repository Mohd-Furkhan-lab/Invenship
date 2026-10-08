from fastapi import HTTPException
from analytics_engine.main import get_full_analysis
from env_loader import load_env
from ollama import Client
from fastmcp import Client as McpClient
import os

load_env()



def getreport(is_admin):
    if is_admin:
        report = get_full_analysis()
        if report is None:
            raise HTTPException(500,detail="Internal Server Error")
        return report



def clean_args(arguments, schema):
    """Keep only the arguments the MCP tool's schema actually allows."""
    allowed = set((schema or {}).get("properties", {}).keys())
    return {k: v for k, v in (arguments or {}).items() if k in allowed}


async def chat_assistant(is_admin, data):

    if is_admin:
        async with McpClient(
            os.getenv("mcp_client")
        ) as mcp:
            tools = await mcp.list_tools()
            ollama_tools = []
            for tool in tools:
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.input_schema
                    }
                })
            client = Client(
                host=os.getenv("ollama_host")
            )
            SYSTEM_PROMPT = """You are the Invenship business assistant for an inventory management system.
                You ONLY help with: sales, inventory, products, purchases and suppliers.
                Rules:
                - For any data question, call the matching tool. Never guess numbers.
                - Tools take no arguments unless their schema lists some.
                - If the user greets you, reply briefly and list what you can help with.
                - If the question is unrelated (jokes, general knowledge, personal chat, coding),
                politely say you can only help with inventory, sales, purchases and suppliers.
                - Keep answers short and base them only on tool results."""
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": data.question}
            ]
            response = client.chat(
                model="llama3.2:3b",
                messages=messages,
                tools=ollama_tools
            )
            if response.message.tool_calls:
                messages.append(response.message)
                for tool_call in response.message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments
                    schema = next(
                        (t.input_schema for t in tools if t.name == tool_name),
                        {}
                    )
                    arguments = clean_args(arguments, schema)
                    result = await mcp.call_tool(
                        tool_name,
                        arguments
                    )
                    messages.append({
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": str(result.data)
                    })
                final_response = client.chat(
                    model="llama3.2:3b",
                    messages=messages
                )
                return final_response.message.content or "I got the data but couldn't summarize it. Please try again."
            return response.message.content or "I can help with sales, inventory, purchases and suppliers. What would you like to know?"
        