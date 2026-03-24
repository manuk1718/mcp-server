import asyncio
import sys
from pathlib import Path
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main() -> None:
    base_dir = Path(__file__).resolve().parent
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["my_server.py"],
        cwd=base_dir,
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            print(f"Connected to my_server.py. Tools: {tool_names}")


if __name__ == "__main__":
    asyncio.run(main())
