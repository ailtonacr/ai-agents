# 👨‍💻 Developer Guide

This guide summarizes the essentials for contributing to the AI Agents Platform.

## Getting Started

1.  **Set up the project:** Follow the [Installation Guide](installation.md) to clone the repository and choose your development setup:
    - **Docker (Recommended)**: `make docker-run` for full stack development
    - **Hybrid**: `docker-compose up db -d` + `make run-dev` for agent development
    - **Local**: Full local setup for advanced development

2.  **Fork the repository:** Create your own fork of the project on GitHub.

3.  **Configure upstream remote:** Add the original repository as the upstream remote to keep your fork updated.
    ```bash
    git remote add upstream https://github.com/ailtonacr/ai-agents.git
    git fetch upstream
    ```

## Development Environments

### Docker Development (Recommended)
```bash
# Full stack with all services
make docker-run

# Access:
# - Web UI: http://localhost:8501
# - Agent API: http://localhost:8000 (via internal network)
# - MySQL: localhost:3306 (external access)

# Development commands
docker-compose logs -f app    # Follow app logs
docker-compose logs -f agent  # Follow agent logs
docker-compose exec app bash  # Access app container shell
```

### Hybrid Development
Best for agent development and testing:
```bash
# Start database only
docker-compose up db -d

# Run agents in development mode
make run-dev

# Access ADK web interface for testing
# http://localhost:8000

# Run UI separately if needed
cd src/app && streamlit run main.py
```

### Local Development
For advanced development requiring full control:
```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
make setup

# Configure local MySQL and environment
# Run components individually
```

## Code Standards
- **Formatting:** Use Black (`make lint`)
- **Architecture:** Follow MVC pattern with clear layer separation
- **Logging:** Use the centralized logging system for all operations (see [logging.md](logging.md))
- **Naming:**
  - Classes: PascalCase (e.g., `UserController`, `ChatComponent`)
  - Functions/variables: snake_case (e.g., `get_user_data`, `session_id`)
  - Constants: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`)
  - Files: snake_case (e.g., `user_controller.py`, `chat_components.py`)
- **Docstrings:** Google style for all public methods
- **Type hints:** Required in all function signatures
- **Imports:** Group by standard library, third-party, then local imports

## Project Structure
```
src/
├── app/                       # Streamlit web application
│   ├── main.py               # Application entry point
│   ├── controller/           # Business logic and routing
│   ├── infrastructure/       # Data access, services, config
│   ├── model/                # Domain entities and validation
│   └── view/                 # UI components and presentations
│       └── components/       # Reusable UI components
├── agents/                   # AI agents (ADK-based)
│   └── bibble/              # Example agent
└── mcp_server/              # Model Context Protocol server
    ├── server.py            # MCP server entry point
    ├── interfaces/          # MCP tool interfaces
    ├── services/            # Business logic for tools
    ├── models/              # Data schemas
    └── scripts/             # Maintenance and setup scripts
```

## Development Guidelines
- **Controllers**: Keep business logic in controllers, not views
- **Components**: Create reusable UI components in `view/components/`
- **Models**: Add validation and business rules to domain models
- **Infrastructure**: Place all external integrations and data access here
- **Factory Pattern**: Use `app_factory.py` for dependency management
- **Logging**: Always add appropriate logs for debugging and monitoring (INFO, WARNING, ERROR levels)
- **Docker First**: Test changes with Docker to ensure production compatibility

## Development Workflow

### Feature Development
```bash
# 1. Start development environment
make docker-run
# or for agent-focused work
make run-dev

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and test
# - Use Docker logs for debugging
# - Test both UI and API functionality
# - Verify database changes persist

# 4. Format and lint
make lint

# 5. Run tests
make test

# 6. Commit and push
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### Testing Changes

#### Docker Testing
```bash
# Rebuild and test changes
docker-compose down
docker-compose up --build

# Test specific components
docker-compose up db agent  # Test without UI
docker-compose logs app     # Check app logs
```

#### Local Testing
```bash
# Test agents independently
make run-dev

# Test UI independently
cd src/app && streamlit run main.py

# Test MCP server
cd src/mcp_server && python server.py
```

## Debugging

### Docker Debugging
```bash
# Access container shells
docker-compose exec app bash
docker-compose exec agent bash

# View real-time logs
docker-compose logs -f

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart app
```

### Application Debugging
- **App logs**: `src/app/logs/app_activity.log` (rotated: `app_activity.log.YYYY-MM-DD`)
- **MCP logs**: `src/mcp_server/logs/mcp_server_activity.log` (rotated: `mcp_server_activity.log.YYYY-MM-DD`)
- **Docker logs**: `docker-compose logs <service>`

## Branching & Workflow
- `main`: Stable code
- `develop`: Integration branch  
- `feature/*`, `bugfix/*`, `hotfix/*`: Topic branches
- Use Conventional Commits (feat, fix, docs, etc.)

## Adding New Features

### Adding a New Agent
1. Create agent directory in `src/agents/your_agent/`
2. Implement agent class and prompts
3. Test with `make run-dev`
4. Add to Docker if needed

### Adding MCP Tools
1. Create tool in `src/mcp_server/interfaces/`
2. Register in `server.py`
3. Test with MCP clients
4. See [MCP Server](mcp_server.md) for details

### Adding RAG Domains
1. Follow the guide in [RAG Module](rag_module.md)
2. Create domain-specific classes
3. Run index creation scripts
4. Test search functionality

## Useful Resources
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Google ADK](https://google.github.io/adk-docs/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Whoosh Documentation](https://whoosh.readthedocs.io/en/latest/index.html)

## Contribution Process
- Open/label issues with details
- Be constructive in code reviews
- Keep commits atomic and clear
- Update docs as needed
- Test with Docker before submitting

## Developer Checklist
- [ ] Read docs and set up environment
- [ ] Choose appropriate development setup (Docker/Hybrid/Local)
- [ ] Run and write tests
- [ ] Follow code and commit standards
- [ ] Add appropriate logging for new features
- [ ] Test changes with Docker
- [ ] Update documentation
- [ ] Review your code before PR

## Help & Support
- GitHub Issues: Bugs/features
- Discussions: General questions
- Email: Sensitive issues

---
For more details, see [Architecture](architecture.md), [Features](features.md), [Installation](installation.md), and [Logging System](logging.md).
