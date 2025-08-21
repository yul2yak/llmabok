from langchain_mcp_adapters.client import MultiServerMCPClient
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["server.py"],
            "transport": "stdio",
        }
    }
)
tools = await client.get_tools()    # asynchronous call to get tools
