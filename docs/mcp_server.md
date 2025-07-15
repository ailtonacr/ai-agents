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

#### Docker (Recommended)
```bash
# MCP server starts automatically with the agent
make docker-run

# Or start only the agent service
docker-compose up agent

# Check MCP server logs
docker-compose logs agent
```

#### Local Development
```bash
# For development and testing
make run-dev

# Or manually
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

## 🐳 Docker Integration

The MCP server runs inside the `adk_agent` container and is automatically started when the agent service starts. This provides:

- **Isolated environment**: Consistent runtime across development and production
- **Automatic dependency management**: All Python packages pre-installed
- **Integrated logging**: Logs accessible via `docker-compose logs agent`
- **Network isolation**: Secure communication within Docker network

## 📊 Monitoring and Debugging

### Docker Environment
```bash
# View MCP server logs
docker-compose logs agent | grep "mcp_server"

# Access container for debugging
docker-compose exec agent bash

# Restart MCP server (restarts entire agent)
docker-compose restart agent
```

### Local Environment
```bash
# Direct log access
tail -f src/mcp_server/logs/mcp_server_activity.log

# Debug mode
cd src/mcp_server
python -u server.py  # Unbuffered output
```

For more details on RAG integration, see [RAG Module](rag_module.md).
For development workflow, see [Development Guide](development.md).
