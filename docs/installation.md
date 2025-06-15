# 📦 Installation

This guide provides step-by-step instructions to install and configure the AI Agents Platform.

## Requirements
- **Python** 3.12+
- **MySQL** 8.0+
- **pip** (comes with Python)
- **Git**

Check prerequisites:
```bash
python --version    # 3.12+
mysql --version     # 8.0+
pip --version
git --version
```

## Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ailtonacr/ai-agents.git
   cd ai-agents
   ```
2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or venv\Scripts\activate  # Windows
   ```
3. **Install dependencies:**
   ```bash
   make setup
   # or
   pip install -r requirements.txt
   ```
4. **Install and configure MySQL:**
   - Ubuntu/Debian:
     ```bash
     sudo apt update && sudo apt install mysql-server
     sudo mysql_secure_installation
     ```
   - macOS:
     ```bash
     brew install mysql
     brew services start mysql
     ```
   - Windows: Download from official site.

5. **Create database and user:**
   ```sql
   CREATE DATABASE ai_agents;
   CREATE USER 'ai_agents_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON ai_agents.* TO 'ai_agents_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
6. **Configure environment variables:**
   - Copy `.env.example` to `.env` and edit as needed:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ai_agents
   DB_USER=ai_agents_user
   DB_PASSWORD=your_secure_password
   GOOGLE_API_KEY=<your-google-api-key>
   # API_BASE_URL=http://localhost:8000
   ```
7. **Initialize database and test:**
   ```bash
   make run-ui  # Starts the web app and initializes tables
   ```

## Verification
- Run `make run-ui` and `make run-agent` in separate terminals to test connectivity.
- Or run `make run` to start all components.

## Troubleshooting
- **MySQL not running:** Check service status (`systemctl` or `brew services`).
- **Dependency errors:** Upgrade pip and reinstall requirements.
- **Port in use:** Use `lsof -i :<port>` and `kill <PID>`.
- **Google ADK issues:** Check `.env` credentials and [official docs](https://google.github.io/adk-docs/).

## Next Steps
- See [Features](features.md)
- See [Architecture](architecture.md)
- See [Developer Guide](development.md)
