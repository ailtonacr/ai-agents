# RAG System (Retrieval-Augmented Generation)

This document describes the RAG system implemented in the AI Agents platform, based on Whoosh for indexing and searching specialized documents by domain.

## Overview
The RAG system enables intelligent search over specific datasets using Whoosh indexing. Each domain (e.g., financial reports) has its own data structure, schema, and specialized search class, following Clean Architecture principles.

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
- Defines fields: TEXT, ID, STORED (for more formats, see the [official documentation](https://whoosh.readthedocs.io/en/latest/index.html))
- Specific configurations such as text analyzers

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
    YOUR_DOMAIN = Path(__file__).parent
    
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
    YOUR_DOMAIN = Path(__file__).parent
    
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

        logger.info(f'{YOUR_DOMAIN} index created successfully')
        
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
    MCP interface for <your_domain> search.
    
    Args:
        query: Search term
        top_k: Maximum number of results
        filters: Optional filters
    
    Returns:
        dict: Search results
    """
    try:
        searcher = <YourDomain>RAGSearcher()
        return searcher.search(query, top_k, filters)
    except Exception as e:
        logger.error(f"Error in <your_domain> search: {e}")
        return {"status": "error", "message": str(e)}

def get_<your_domain>_filters() -> dict:
    """Returns available filters for <your_domain>"""
    try:
        searcher = <YourDomain>RAGSearcher()
        return searcher.get_available_filters()
    except Exception as e:
        logger.error(f"Error getting <your_domain> filters: {e}")
        return {"status": "error", "message": str(e)}
```

### 5. Register in MCP Server

Edit `src/mcp_server/interfaces/__init__.py` before include your function in MCP Server.

```python
# Add all your functions for import in 'server.py'
from .rag_<your_domain> import (
    rag_<your_domain>_search,
    rag_<your_domain>_filters
)
```

Edit `src/mcp_server/server.py` to include your functions:

```python
# Add import
from interfaces import (
    rag_<your_domain>_search,
    get_<your_domain>_filters
)

# Add to ADK_TOOLS dictionary
ADK_TOOLS = {
    "rag_<your_domain>_search": FunctionTool(func=rag_<your_domain>_search),
    "get_<your_domain>_filters": FunctionTool(func=get_<your_domain>_filters),
    # ... other tools
}
```

## JSON Data Example

Your JSON data should follow this structure for optimal indexing:

```json
[
  {
    "id": "doc_001",
    "title": "Monthly Revenue Report",
    "category": "financial",
    "date": "2024-01",
    "content": "This document contains detailed revenue analysis for January 2024. Total revenue reached $150,000 with a 15% increase compared to previous month."
  },
  {
    "id": "doc_002", 
    "title": "Quarterly Expenses Summary",
    "category": "financial",
    "date": "2024-Q1",
    "content": "Comprehensive breakdown of operational expenses for Q1 2024. Major categories include personnel costs, infrastructure, and marketing investments."
  }
]
```

## Implementation Flow

1. **Prepare data**: Organize your data in JSON format in `data/src/<your_domain>/`
2. **Define schema**: Create model with appropriate fields for your domain
3. **Implement searcher**: Inherit from BaseRAGSearcher and specialize as needed
4. **Create scripts**: Implement create_index.py and update_index.py
5. **Execute indexing**: Run creation script to generate initial index
6. **Create MCP interface**: Implement functions for MCP exposure
7. **Register in server**: Add tools to MCP server
8. **Test**: Validate search and filters working correctly

## Usage Examples

```python
# Simple search
searcher = YourDomainRAGSearcher()
results = searcher.search("search term", top_k=3)

# Search with filters
results = searcher.search(
    "search term", 
    top_k=5, 
    filter_by={"category": "example", "date": "2024"}
)

# Get available filters
filters = searcher.get_available_filters()
```

## Important Notes

- Always run create_index.py before first search
- Use update_index.py to add new data without recreating the index
- Logs are automatically recorded via centralized logging system
- Whoosh schemas define indexable and searchable fields
- Filters should be defined as ID or TEXT fields in schema
- System supports specific analyzers (e.g., Portuguese)

## References

- **Whoosh Documentation**: [https://whoosh.readthedocs.io/en/latest/index.html](https://whoosh.readthedocs.io/en/latest/index.html)
- **Whoosh Schema Guide**: [https://whoosh.readthedocs.io/en/latest/schema.html](https://whoosh.readthedocs.io/en/latest/schema.html)
- **Whoosh Searching**: [https://whoosh.readthedocs.io/en/latest/searching.html](https://whoosh.readthedocs.io/en/latest/searching.html)

---

For more details about architecture, see [architecture.md](architecture.md) and [mcp_server.md](mcp_server.md).
