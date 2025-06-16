# 👨‍💻 Developer Guide

This guide summarizes the essentials for contributing to the AI Agents Platform.

## Getting Started

1.  **Set up the project:** Follow the [Installation Guide](installation.md) to clone the repository, set up your virtual environment, and install dependencies.
2.  **Fork the repository:** Create your own fork of the project on GitHub.
3.  **Configure upstream remote:** Add the original repository as the upstream remote to keep your fork updated.
    ```bash
    git remote add upstream https://github.com/ailtonacr/ai-agents.git
    git fetch upstream
    ```

## Code Standards
- **Formatting:** Use Black (`make lint`)
- **Architecture:** Follow MVC pattern with clear layer separation
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
src/app/
├── main.py                    # Application entry point
├── controller/                # Business logic and routing
├── infrastructure/            # Data access, services, config
├── model/                     # Domain entities and validation
└── view/                      # UI components and presentations
    └── components/            # Reusable UI components
```

## Development Guidelines
- **Controllers**: Keep business logic in controllers, not views
- **Components**: Create reusable UI components in `view/components/`
- **Models**: Add validation and business rules to domain models
- **Infrastructure**: Place all external integrations and data access here
- **Factory Pattern**: Use `app_factory.py` for dependency management

## Branching & Workflow
- `main`: Stable code
- `develop`: Integration branch
- `feature/*`, `bugfix/*`, `hotfix/*`: Topic branches
- Use Conventional Commits (feat, fix, docs, etc.)

## Useful Resources
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Google ADK](https://google.github.io/adk-docs/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [bcrypt](https://pypi.org/project/bcrypt/)

## Contribution Process
- Open/label issues with details
- Be constructive in code reviews
- Keep commits atomic and clear
- Update docs as needed

## Developer Checklist
- [ ] Read docs and set up environment
- [ ] Run and write tests
- [ ] Follow code and commit standards
- [ ] Update documentation
- [ ] Review your code before PR

## Help & Support
- GitHub Issues: Bugs/features
- Discussions: General questions
- Email: Sensitive issues

---
For more details, see [Architecture](architecture.md) and [Features](features.md).
