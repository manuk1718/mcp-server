from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server")
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()