# 🔧 MCP Server

This document describes the MCP (Model Context Protocol) server implementation.

## 📋 Overview

The MCP Server provides a standardized interface for integrating tools and functionalities through the Model Context Protocol, enabling communication between AI clients and server-side tools.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│ MCP Client (Claude Desktop, AI Tools, etc.)             │
├─────────────────────────────────────────────────────────┤
│ MCP Protocol (stdio transport)                          │
├─────────────────────────────────────────────────────────┤
│ MCP Server (server.py)                                  │
│ ├─ Tool Registry (ADK_TOOLS)                            │
│ ├─ Handler: @app.list_tools()                           │
│ └─ Handler: @app.call_tool()                            │
├─────────────────────────────────────────────────────────┤
│ ADK Tools Integration                                   │
│ RAG System Integration                                  │
├─────────────────────────────────────────────────────────┤
│ Infrastructure (logging, config)                        │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Features

- **Standard Protocol**: Implements Model Context Protocol specification
- **ADK Integration**: Converts Google ADK tools to MCP format using `adk_to_mcp_tool_type`
- **RAG Tools**: Exposes domain-specific RAG search capabilities (see [RAG System](rag_module.md))
- **Transport Layer**: Communication via stdio (standard input/output)
- **Async Execution**: Uses asyncio for non-blocking operations
- **Error Handling**: Structured error responses and comprehensive logging
- **Tool Registry**: Dictionary-based tool management (`ADK_TOOLS`)

## 📁 Structure

```
src/mcp_server/
├── server.py                      # Main MCP server implementation
├── infrastructure/
│   ├── __init__.py
│   └── logging_config.py          # Logging configuration
├── interfaces/                    # Integration interfaces for tools
├── services/                      # Business logic and services
├── models/                        # Data models and schemas
├── scripts/                       # Utility and maintenance scripts
├── data/                          # Supporting data and files
│   ├── indexes/<domain>/          # Index files for RAG by domain
│   └── src/<domain>/              # Raw data for RAG create by domain
└── logs/
    ├── mcp_server_activity.log    # Current log file
    └── mcp_server_activity_*.log  # Rotated log files
```

## 🚀 Usage

### Starting the Server

```bash
cd src/mcp_server
python server.py
```

### Client Configuration

Configure MCP clients to connect using:

```python
 tools=[
    MCPToolset(
        connection_params=StdioServerParameters(
            command="python3",
            args=["src/mcp_server/server.py"],
        )
    )
],
```

## 🔧 Implementation

### Tool Registration

Tools are registered in the `ADK_TOOLS` dictionary:

```python
ADK_TOOLS = {
    "my_tool": FunctionTool(func=my_tool),
}
```

### Server Handlers

The server implements two main MCP handlers:

- **`@app.list_tools()`**: Returns available tools in MCP format
- **`@app.call_tool()`**: Executes requested tools and returns responses

### Tool Execution Flow

1. Client requests tool execution via MCP protocol
2. Server looks up tool in `ADK_TOOLS` registry
3. Tool is executed asynchronously using `run_async()`
4. Response is formatted as JSON and returned to client

## 📊 Monitoring

The server logs all activities including:
- Tool registration and discovery
- Client connections and requests
- Tool execution results and errors
- Server lifecycle events

Log files are stored in `src/mcp_server/logs/` with daily rotation.

## 🔄 Extending

### Adding New Tools

1. **Define your function**:
```python
def my_tool(param: str) -> str:
    return f"Processed: {param}"
```

2. **Register in `ADK_TOOLS`**:
```python
ADK_TOOLS = {
    "my_tool": FunctionTool(func=my_tool),
}
```

### Function Requirements

#### Function Signature
- Functions must have **type hints** for all parameters
- Return type should be specified
- Parameters become the tool's input schema automatically

```python
def calculate_sum(a: int, b: int) -> dict:
    """Calculate the sum of two numbers."""
    return {
        "result": a + b,
        "operation": "sum"
    }
```

#### Parameter Types
Supported parameter types for MCP tools:
- `str` - String values
- `int` - Integer numbers  
- `float` - Decimal numbers
- `bool` - Boolean values
- `dict` - JSON objects
- `list` - Arrays
- Optional parameters: `param: str = "default"`

#### Return Values
Functions can return:
- **Primitive types**: `str`, `int`, `float`, `bool`
- **Dictionaries**: JSON-serializable objects
- **Lists**: Arrays of serializable data
- **Complex objects**: Must be JSON-serializable

```python
# Simple return
def get_status() -> str:
    return "Server is running"

# Structured return
def get_user_info(user_id: int) -> dict:
    return {
        "id": user_id,
        "name": "John Doe",
        "active": True
    }
```

#### Function Documentation
Use docstrings to provide tool descriptions:

```python
def weather_info(city: str, units: str = "metric") -> dict:
    """Get weather information for a city.
    
    Args:
        city (str): Name of the city.
        units (str): Temperature units (metric, imperial).
    
    Returns:
        dict: Weather data including temperature and conditions.
    """
    return {
        "city": city,
        "temperature": 22,
        "units": units,
        "condition": "sunny"
    }
```

### Tool Execution

When a client calls a tool, the MCP server:

1. **Validates parameters** against function signature
2. **Calls the function** with provided arguments
3. **Serializes the response** to JSON
4. **Wraps in MCP format** (`TextContent`)
5. **Returns to client** via stdio


### Model Context Protocol (MCP)

#### Official Documentation
- **[MCP Specification](https://spec.modelcontextprotocol.io/)** - Complete protocol specification
- **[MCP Website](https://modelcontextprotocol.io/)** - Main project website and overview
- **[MCP GitHub Repository](https://github.com/modelcontextprotocol)** - Source code and examples

#### Implementation Resources
- **[MCP Python SDK](https://pypi.org/project/mcp/)** - Python library for MCP implementation
- **[MCP TypeScript SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk)** - TypeScript/JavaScript SDK
