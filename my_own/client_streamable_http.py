import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main() -> None:
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = os.getenv("PORT", "8000")
    url = os.getenv("MCP_SERVER_URL", f"http://{host}:{port}/mcp")

    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            print(f"Connected to {url}")
            print(f"Available tools: {tool_names}")


if __name__ == "__main__":
    asyncio.run(main())
