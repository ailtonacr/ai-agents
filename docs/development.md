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
- **Naming:**
  - Classes: PascalCase
  - Functions/variables: snake_case
  - Constants: UPPER_SNAKE_CASE
- **Docstrings:** Google style
- **Type hints:** Required in all functions

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
