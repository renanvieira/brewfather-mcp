import asyncio
from brewfather_mcp.server import mcp

if __name__ == "__main__":
    loop = asyncio.get_running_loop()
    loop.run_until_complete(mcp.run_stdio_async())
