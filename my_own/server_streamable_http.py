import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-streamable-http")
mcp.settings.port = int(os.getenv("PORT", "8000"))


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
