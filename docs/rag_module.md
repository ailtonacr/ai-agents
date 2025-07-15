# RAG System (Retrieval-Augmented Generation)

This document describes the RAG system implemented in the AI Agents platform, based on Whoosh for indexing and searching specialized documents by domain.

## Overview
The RAG system enables intelligent search over specific datasets using Whoosh indexing. Each domain (e.g., financial reports) has its own data structure, schema, and specialized search class, following Clean Architecture principles.

For detailed information about Whoosh features and advanced usage, see the [official Whoosh documentation](https://whoosh.readthedocs.io/en/latest/index.html).

## System Architecture

```
src/mcp_server/
├── models/
│   └── rag_<domain>.py              # Whoosh schema for domain
├── services/
│   ├── base_rag_searcher.py         # Abstract base class
│   ├── <domain>_rag_searcher.py     # Specialized implementation
│   └── rag_manager.py               # Index manager
├── scripts/
│   └── <domain>/
│       ├── create_index.py          # Initial index creation
│       └── update_index.py          # Index updates
├── interfaces/
│   └── rag_<domain>.py              # MCP interface for domain
├── data/
│   ├── src/<domain>/                # Raw data (JSON)
│   └── indexes/<domain>/            # Whoosh indexes
└── server.py                        # MCP tools registration
```

## 🐳 Docker Integration

The RAG system runs seamlessly within the Docker environment:

### Running RAG Scripts with Docker
```bash
# Create indexes using Docker
docker-compose exec agent python src/mcp_server/scripts/finance_reports/create_index.py

# Update indexes using Docker
docker-compose exec agent python src/mcp_server/scripts/finance_reports/update_index.py

# Access container for manual operations
docker-compose exec agent bash
```

### Local Development
```bash
# For development and testing
make run-dev

# Run scripts locally
cd src/mcp_server
python scripts/finance_reports/create_index.py
```

## Core Components

### RAGManager
Centralized class that manages Whoosh index creation and updates:
- **create_index()**: Creates index from scratch using JSON data
- **update_index()**: Adds new documents to existing index

### BaseRAGSearcher
Abstract class that defines the common interface for RAG searches:
- **search()**: Executes search with optional filters
- **discover_filterable_values()**: Discovers unique values for filters

### Domain Schema
Models that define Whoosh data structure (e.g., RAGFinanceReports):
- Inherits from Whoosh's SchemaClass
- Defines fields: TEXT, ID, STORED (for more field types, see the [official documentation](https://whoosh.readthedocs.io/en/latest/index.html))
- Specific configurations such as text analyzers

## Data Format Example

The RAG system expects JSON files with the following structure:

```json
[
  {
    "id": "report_2024_001",
    "title": "Quarterly Financial Report Q1 2024",
    "category": "quarterly",
    "date": "2024-03-31",
    "content": "Revenue increased by 15% compared to the previous quarter...",
    "metadata": {
      "department": "finance",
      "confidentiality": "internal",
      "author": "Financial Team"
    }
  },
  {
    "id": "report_2024_002", 
    "title": "Annual Budget Analysis 2024",
    "category": "annual",
    "date": "2024-12-31",
    "content": "The annual budget shows positive trends in operational efficiency...",
    "metadata": {
      "department": "finance",
      "confidentiality": "public",
      "author": "CFO Office"
    }
  }
]
```

## Getting Started: Creating a New RAG Domain

### 1. Define Domain Schema

Create `src/mcp_server/models/rag_<your_domain>.py`:

```python
from whoosh.fields import SchemaClass, TEXT, ID, STORED
from utils.analyser_helper import get_portuguese_analyzer

ANALYZER = get_portuguese_analyzer()

class RAG<YourDomain>(SchemaClass):
    id = TEXT(stored=True)
    # Domain-specific fields
    title = TEXT(stored=True, analyzer=ANALYZER)
    category = ID(stored=True)
    date = TEXT(stored=True, sortable=True)
    content = TEXT(stored=True, analyzer=ANALYZER)
    original_data = STORED
```

### 2. Create Specialized Search Class

Create `src/mcp_server/services/<your_domain>_rag_searcher.py`:

```python
from pathlib import Path
from .base_rag_searcher import BaseRAGSearcher
from infrastructure.logging_config import logger

ROOT_DIR = Path(__file__).parent.parent
INDEX_PATH = ROOT_DIR / "data" / "indexes" / "<your_domain>"

class <YourDomain>RAGSearcher(BaseRAGSearcher):
    FILTERABLE_FIELDS = ['category', 'date']  # Fields for filtering
    
    def __init__(self, index_dir: Path = INDEX_PATH):
        searchable_fields = ["title", "content"]  # Text search fields
        
        super().__init__(
            index_dir=index_dir,
            search_fields=searchable_fields,
            default_operator="OR"
        )
        logger.info(f"{self.__class__.__name__} configured and ready.")
    
    def search(self, query_string: str, top_k: int = 5, filter_by: dict = None) -> dict:
        """Specialized search for <your_domain>"""
        return super().search(query_string, top_k, filter_by)
    
    def get_available_filters(self) -> dict:
        """Returns available filters for <your_domain>"""
        return super().discover_filterable_values(self.FILTERABLE_FIELDS)
```

### 3. Implement Creation and Update Scripts

**Creation Script** - `src/mcp_server/scripts/<your_domain>/create_index.py`:

```python
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from models.rag_<your_domain> import RAG<YourDomain>
from services.rag_manager import RAGManager
from infrastructure.logging_config import logger

if __name__ == "__main__":
    DATA_DIR = ROOT_DIR / "data"

    # Automatically picks up your domain name (matches your folder name).
    YOUR_DOMAIN = Path(__file__).parent.name
    
    # Path to source JSON data
    SOURCE_JSON_PATH = DATA_DIR / "src" / YOUR_DOMAIN / "data.json"
    
    # Index directory
    INDEX_DIR_PATH = DATA_DIR / "indexes" / YOUR_DOMAIN

    logger.info(f'Starting "{YOUR_DOMAIN}" index create')
    
    try:
        schema = RAG<YourDomain>()
        rag_manager = RAGManager()
        
        rag_manager.create_index(
            index_dir=INDEX_DIR_PATH,
            json_input_path=SOURCE_JSON_PATH,
            schema=schema
        )

        logger.info(f'{YOUR_DOMAIN} index created successfully')
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"Failed to create index: {e}")
```

**Update Script** - `src/mcp_server/scripts/<your_domain>/update_index.py`:

```python
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from services.rag_manager import RAGManager
from infrastructure.logging_config import logger

if __name__ == "__main__":
    DATA_DIR = ROOT_DIR / "data"

    # Automatically picks up your domain name (matches your folder name).
    YOUR_DOMAIN = Path(__file__).parent.name
    
    # New data to add
    NEW_DATA_JSON_PATH = DATA_DIR / "src" / YOUR_DOMAIN / "new_data.json"
    
    # Existing index directory
    INDEX_DIR_PATH = DATA_DIR / "indexes" / YOUR_DOMAIN
    
    logger.info(f'Starting "{YOUR_DOMAIN}" index update')
    try:
        rag_manager = RAGManager()
        
        rag_manager.update_index(
            index_dir=INDEX_DIR_PATH,
            json_input_path=NEW_DATA_JSON_PATH
        )

        logger.info(f'{YOUR_DOMAIN} index updated successfully')
        
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
    except Exception as e:
        logger.error(f'Failed to update index: {e}')
```

### 4. Create MCP Interface

Create `src/mcp_server/interfaces/rag_<your_domain>.py`:

```python
from services.<your_domain>_rag_searcher import <YourDomain>RAGSearcher
from infrastructure.logging_config import logger

def rag_<your_domain>_search(query: str, top_k: int = 5, filters: dict = None) -> dict:
    """
    Search <your_domain> documents using RAG.
    
    Args:
        query: Search query string
        top_k: Number of results to return (default: 5)
        filters: Dictionary of filters to apply (optional)
    
    Returns:
        Dictionary with search results and metadata
    """
    try:
        searcher = <YourDomain>RAGSearcher()
        results = searcher.search(query, top_k, filters)
        return results
    except Exception as e:
        logger.error(f"Error in <your_domain> RAG search: {e}")
        return {"error": str(e), "results": []}

def get_<your_domain>_filters() -> dict:
    """Get available filters for <your_domain> search."""
    try:
        searcher = <YourDomain>RAGSearcher()
        return searcher.get_available_filters()
    except Exception as e:
        logger.error(f"Error getting <your_domain> filters: {e}")
        return {"error": str(e)}
```

### 5. Register Tools in MCP Server

Add your new tools to `src/mcp_server/server.py`:

```python
from interfaces.rag_<your_domain> import rag_<your_domain>_search, get_<your_domain>_filters

# Add to ADK_TOOLS dictionary
ADK_TOOLS = {
    # ...existing tools...
    "rag_<your_domain>_search": FunctionTool(func=rag_<your_domain>_search),
    "get_<your_domain>_filters": FunctionTool(func=get_<your_domain>_filters),
}
```

## 🔧 Development Workflow

### Docker Development
```bash
# Start full development environment
make docker-run

# Execute RAG scripts inside container
docker-compose exec agent python src/mcp_server/scripts/<domain>/create_index.py
docker-compose exec agent python src/mcp_server/scripts/<domain>/update_index.py

# Access container for debugging
docker-compose exec agent bash
```

### Local Development  
```bash
# Start agents in development mode
make run-dev

# Run RAG scripts locally
cd src/mcp_server
python scripts/<domain>/create_index.py
python scripts/<domain>/update_index.py
```

## 📚 External Resources

- [Whoosh Official Documentation](https://whoosh.readthedocs.io/en/latest/index.html) - Complete reference for Whoosh features
- [Whoosh Field Types](https://whoosh.readthedocs.io/en/latest/schema.html) - Available field types and options
- [Whoosh Query Language](https://whoosh.readthedocs.io/en/latest/querylang.html) - Advanced query syntax
- [Whoosh Analysis](https://whoosh.readthedocs.io/en/latest/analysis.html) - Text analysis and tokenization

## Best Practices

1. **Schema Design**: Define clear, searchable fields with appropriate analyzers
2. **Data Structure**: Use consistent JSON structure for your domain
3. **Index Management**: Use the provided scripts for index operations
4. **Clean Architecture**: Follow the established patterns for new domains
5. **Testing**: Test both index creation and search functionality
6. **Docker Integration**: Use Docker for consistent environments
7. **Error Handling**: Always include proper error handling and logging

## Troubleshooting

### Common Issues
- **Index creation fails**: Check JSON data format and file paths
- **Search returns no results**: Verify index exists and contains data
- **Import errors**: Ensure Python path includes project root
- **Permission errors**: Check file/directory permissions in Docker

### Debug Commands
```bash
# Check index status (Docker)
docker-compose exec agent ls -la src/mcp_server/data/indexes/<domain>/

# Check logs (Docker)
docker-compose logs agent

# Manual testing (Local)
cd src/mcp_server
python -c "from services.<domain>_rag_searcher import <Domain>RAGSearcher; s = <Domain>RAGSearcher(); print(s.search('test'))"
```

For more information on development workflow, see [Development Guide](development.md).
For MCP server integration, see [MCP Server](mcp_server.md).
