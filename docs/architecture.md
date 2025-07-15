# 🏗️ System Architecture

This document describes the architecture of the AI Agents Platform.

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ Docker Container: streamlit_app                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Presentation Layer (Streamlit Views)                │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ Business Layer (Controllers)                        │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ Infrastructure Layer (DAOs, Services, ADK Client)   │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ Domain Layer (Models)                               │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            │ HTTP API calls (agent:8000)
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Docker Container: adk_agent                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Google ADK API Server (0.0.0.0:8000)               │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ MCP Server (Model Context Protocol)             │ │ │
│ │ │ - Tool exposure via MCP protocol                │ │ │
│ │ │ - RAG system integration                        │ │ │
│ │ │ - stdio transport                               │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            │ MySQL connection (db:3306)
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Docker Container: mysql_db                              │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ MySQL 8.0 Database                                  │ │
│ │ - User management                                   │ │
│ │ - Session storage                                   │ │
│ │ - Message history                                   │ │
│ │ - Automatic healthcheck                             │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🐳 Deployment Architecture

### Production Deployment (Docker)
```
External Network ────► Load Balancer/Reverse Proxy
                                │
                                ▼
                        ┌─────────────────┐
                        │ Docker Network  │
                        │ ai_platform_net │
                        └─────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│streamlit_app│        │ adk_agent   │        │  mysql_db   │
│   :8501     │◄──────►│   :8000     │◄──────►│   :3306     │
│             │        │             │        │             │
│ - Web UI    │        │ - ADK API   │        │ - Database  │
│ - Auth      │        │ - MCP Tools │        │ - Persistence│
│ - Chat      │        │ - Agents    │        │ - Health    │
└─────────────┘        └─────────────┘        └─────────────┘
```

### Development Setup Options

#### Docker Development (Recommended)
```bash
make docker-run  # Full stack with hot reload
# - All services in containers
# - Shared volumes for development
# - Database persistence
```

#### Hybrid Development
```bash
docker-compose up db -d  # Database only
make run-dev            # Agents locally with ADK web UI
# - Database in container
# - Agents running locally
# - Best for agent development
```

#### Local Development
```bash
# All components running locally
# - Full control over environment
# - Manual MySQL setup required
# - Direct file access
```
