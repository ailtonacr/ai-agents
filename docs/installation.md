# 📦 Installation

This guide provides step-by-step instructions to install and configure the AI Agents Platform.

## 🐳 Quick Start with Docker (Recommended)

The easiest way to run the AI Agents Platform is using Docker, which handles all dependencies automatically.

### Requirements
- **Docker** and **Docker Compose**
- **Git**

Check prerequisites:
```bash
docker --version       # 20.0+
docker-compose --version  # 2.0+
git --version
```

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ailtonacr/ai-agents.git
   cd ai-agents
   ```

2. **Configure environment variables:**
   ```bash
   # Create .env file with your Google API key
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

3. **Run with Docker:**
   ```bash
   make docker-run
   # or
   docker-compose up --build
   ```

4. **Access the application:**
   - **Web UI**: http://localhost:8501
   - The database and all services start automatically
   - Tables are created on first run

### Stopping the Application
```bash
make docker-stop
# or
docker-compose down
```

## 🛠️ Local Development Setup

For developers who want to run components individually or contribute to the project.

### Requirements
- **Python** 3.12+
- **MySQL** 8.0+ (optional - Docker can handle this)
- **pip** (comes with Python)
- **Git**

### Development Options

#### Option 1: Hybrid (Docker DB + Local Development)
Best for development work:

```bash
# Start only the database with Docker
docker-compose up db -d

# Run agents locally for development
make run-dev

# Run UI locally (in another terminal)
cd src/app
streamlit run main.py
```

#### Option 2: Full Local Setup
Complete local installation:

1. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   make setup
   # or
   pip install -r requirements.txt
   ```

3. **Install and configure MySQL:**
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

4. **Create database and user:**
   ```sql
   CREATE DATABASE chat_db;
   CREATE USER 'dev'@'localhost' IDENTIFIED BY 'dev';
   GRANT ALL PRIVILEGES ON chat_db.* TO 'dev'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configure environment variables:**
   ```env
   MYSQL_HOST=localhost
   MYSQL_USER=dev
   MYSQL_PASSWORD=dev
   MYSQL_DATABASE=chat_db
   GOOGLE_API_KEY=your_google_api_key_here
   API_BASE_URL=http://localhost:8000
   ```

6. **Run components separately:**
   ```bash
   # Terminal 1: Run agents
   make run-dev
   
   # Terminal 2: Run UI
   cd src/app && streamlit run main.py
   ```

## 🔍 Development Commands

### Available Make Commands
```bash
make setup          # Install Python dependencies
make lint           # Format code with Black
make test           # Run unit tests with coverage
make run-dev        # Run agents in development mode (no UI)
make docker-run     # Start full application with Docker
make docker-stop    # Stop Docker containers
```

### Understanding `make run-dev`
This command runs only the agents in development mode using ADK's web interface:
- **Purpose**: Development and testing of agents without the full UI
- **Access**: http://localhost:8000 (ADK web interface)
- **Use case**: Agent development, testing prompts, debugging MCP tools
- **Requirements**: Local Python environment with dependencies installed

## 📊 Verification

### Docker Setup
```bash
# Check if containers are running
docker-compose ps

# Check logs
docker-compose logs

# Check specific service
docker-compose logs app
```

### Local Setup
```bash
# Test database connection
mysql -h localhost -u dev -pdev chat_db -e "SELECT 1;"

# Test Python dependencies
python -c "import streamlit, mysql.connector; print('Dependencies OK')"

# Check agent API
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Docker Issues
- **Port conflicts**: Check if ports 8501, 8000, or 3306 are in use
- **Permission errors**: Ensure Docker daemon is running
- **Build failures**: Try `docker-compose down && docker-compose up --build`

### Local Development Issues
- **MySQL not running**: Check service status (`systemctl` or `brew services`)
- **Dependency errors**: Upgrade pip and reinstall requirements
- **Port in use**: Use `lsof -i :<port>` and `kill <PID>`
- **Google ADK issues**: Check `.env` credentials and [official docs](https://google.github.io/adk-docs/)

### Application Issues
- **Database connection**: Check environment variables and database status
- **Agent communication**: Verify ADK is running and accessible
- **UI not loading**: Check Streamlit logs and network configuration

### Log Locations
- **Docker**: `docker-compose logs <service_name>`
- **Local App**: `src/app/logs/app_activity.log` (rotated files: `app_activity.log.YYYY-MM-DD`)
- **Local MCP**: `src/mcp_server/logs/mcp_server_activity.log` (rotated files: `mcp_server_activity.log.YYYY-MM-DD`)

## 🔧 Production Considerations

### Docker Production Setup
```bash
# Use production docker-compose (if available)
docker-compose -f docker-compose.prod.yml up -d

# Check resource usage
docker stats

# Monitor logs
docker-compose logs -f --tail=100
```

### Environment Variables for Production
```env
# Security
MYSQL_ROOT_PASSWORD=secure_random_password
MYSQL_PASSWORD=secure_random_password

# Performance
MYSQL_INNODB_BUFFER_POOL_SIZE=1G

# Monitoring
LOG_LEVEL=INFO
```

## 📚 Next Steps
- See [Features](features.md) for usage guide
- See [Architecture](architecture.md) for system overview
- See [Development](development.md) for contribution guidelines
- See [Logging System](logging.md) for monitoring and debugging
