# Bookmark Manager Technical Specification

## Table of Contents

1. [Introduction](#introduction)
2. [Python Idiomatic Practices](#python-idiomatic-practices)
3. [Version Control Guidelines](#version-control-guidelines)
4. [Dependency Management with UV](#dependency-management-with-uv)
5. [Code Quality Assurance](#code-quality-assurance)
6. [Environment Configuration](#environment-configuration)
7. [Logging](#logging)
8. [Exception Handling](#exception-handling)
9. [Documentation](#documentation)
10. [Testing Strategy](#testing-strategy)
11. [Security Best Practices](#security-best-practices)

## Introduction

This technical specification serves as the definitive guide for development practices on the Bookmark Manager project. All contributors should adhere to these guidelines to ensure code consistency, maintainability, and quality.

## Python Idiomatic Practices

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Limit lines to 120 characters
- Use snake_case for functions and variables, PascalCase for classes

### Naming Conventions

✅ **Good:**
```python
def extract_metadata(url: str) -> dict:
    """Extract metadata from a URL."""
    page_content = fetch_page(url)
    return parse_content(page_content)

class BookmarkRepository:
    """Repository for bookmark operations."""
```

❌ **Bad:**
```python
def ExtractMetadata(theUrl: str) -> dict:
    """Extract metadata from a URL."""
    content = fetch_page(theUrl)  # Inconsistent naming
    return parse_content(content)

class bookmarkRepo:  # Inconsistent casing
    """Repository for bookmark operations."""
```

### Type Hints

- Always use type hints for function parameters and return values
- Use `Optional[Type]` for parameters that might be None
- Use `->` to indicate return type, including `-> None` when appropriate

✅ **Good:**
```python
from typing import Optional, List, Dict, Any

def parse_bookmark_file(file_path: str) -> List[Dict[str, Any]]:
    """Parse a bookmark file and return a list of bookmarks."""
    # ...
    return bookmarks

def get_bookmark_by_id(bookmark_id: int) -> Optional[Dict[str, Any]]:
    """Get a bookmark by ID, returning None if not found."""
    # ...
    return bookmark if bookmark else None
```

### Docstrings

- Use docstrings for all public modules, functions, classes, and methods
- Follow Google style docstrings format

✅ **Good:**
```python
def classify_bookmark(url: str, title: str, content: str) -> List[str]:
    """Classify a bookmark into categories using the LLM.

    Args:
        url: The bookmark URL
        title: The page title
        content: The page content

    Returns:
        List of category tags

    Raises:
        ClassificationError: If classification fails
    """
```

### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application imports
- Use separate lines for each import

✅ **Good:**
```python
import os
import sys
from typing import Dict, List, Optional

import click
import requests
from bs4 import BeautifulSoup

from bookmark_manager.models import BookmarkModel
from bookmark_manager.utils import extract_metadata
```

## Version Control Guidelines

### Branch Naming Convention

- `feature/short-description` - For new features
- `bugfix/issue-number-description` - For bug fixes
- `refactor/component-name` - For code refactoring
- `docs/topic` - For documentation updates

### Commit Messages

- Use the imperative mood ("Add feature" not "Added feature")
- First line is a summary (50 chars or less)
- Optional detailed explanation after a blank line
- Reference issue numbers at the end

✅ **Good:**
```
Add bookmark classification using DistilBERT

- Implement model initialization with caching
- Add preprocessing pipeline for text normalization
- Create confidence threshold for categories

Closes #42
```

❌ **Bad:**
```
I added some stuff for the bookmark system and fixed bugs
```

### Pull Request Guidelines

- Create PR against the `main` branch
- Use the PR template
- Include detailed description of changes
- Link to relevant issues
- Ensure all CI checks pass
- Request review from at least one team member
- PRs should ideally represent a single logical change

## Dependency Management with UV

### Setup

- Use [UV](https://github.com/astral-sh/uv) as the package manager
- Keep virtual environments project-specific

### Project Setup

```bash
# Create a new virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # Unix/Linux
.venv\Scripts\activate     # Windows
```

### Dependency Specification

- Use `pyproject.toml` for project metadata and dependencies
- Maintain `requirements.in` for direct dependencies
- Generate `requirements.txt` for pinned versions

```toml
# pyproject.toml example
[project]
name = "bookmark_manager"
version = "0.1.0"
description = "Intelligent bookmark management system"
requires-python = ">=3.10"
dependencies = [
    "click>=8.1.0",
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0",
    "transformers>=4.25.0",
    "python-telegram-bot>=13.0",
    "ruff>=0.0.260",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pre-commit>=3.0.0",
    "mkdocs>=1.4.0",
    "mkdocs-material>=9.0.0",
]
```

### Common UV Commands

```bash
# Install all dependencies
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"

# Compile pinned dependencies
uv pip compile requirements.in -o requirements.txt

# Add a package
uv add requests

# Upgrade a package
uv sync --upgrade-package beautifulsoup4
```

## Code Quality Assurance

- Use Ruff for linting and formatting
- Set up pre-commit hooks to ensure code quality before committing

## Environment Configuration

### Environment Variables

- Use environment variables for configuration that varies by environment
- Leverage `.env` files for local development (but never commit them)
- Use a library like `python-dotenv` to load from `.env` files

```python
# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configuration with defaults
DB_PATH = os.environ.get("BOOKMARK_DB_PATH", "./bookmarks.db")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
MODEL_CACHE_DIR = os.environ.get("MODEL_CACHE_DIR", "./models")
```

### Secrets Management

✅ **Good:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_telegram_client():
    """Create authenticated Telegram client."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
    return TelegramClient(token)
```

❌ **Bad:**
```python
def get_telegram_client():
    """Create authenticated Telegram client."""
    # NEVER do this
    token = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
    return TelegramClient(token)
```

## Logging

### Basic Setup

```python
# logging_config.py
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(app_name: str, log_level: str = "INFO") -> None:
    """Configure application logging.

    Args:
        app_name: Application name for log identification
        log_level: Minimum log level to capture
    """
    log_dir = os.environ.get("LOG_DIR", "./logs")
    os.makedirs(log_dir, exist_ok=True)

    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    simple_formatter = logging.Formatter("%(levelname)s - %(message)s")

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(simple_formatter)

    # Configure file handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, f"{app_name}.log"),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(detailed_formatter)

    # Add handlers to root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
```

### Usage Examples

✅ **Good:**
```python
import logging

logger = logging.getLogger(__name__)

def process_bookmark(url: str) -> bool:
    """Process a bookmark URL.

    Args:
        url: The bookmark URL to process

    Returns:
        True if successful, False otherwise
    """
    logger.info("Processing bookmark: %s", url)
    try:
        metadata = extract_metadata(url)
        logger.debug("Extracted metadata: %s", metadata)
        return True
    except Exception as e:
        logger.error("Failed to process bookmark: %s", url, exc_info=True)
        return False
```

❌ **Bad:**
```python
def process_bookmark(url: str) -> bool:
    """Process a bookmark URL."""
    print(f"Processing {url}")  # Don't use print for logging
    try:
        metadata = extract_metadata(url)
        return True
    except Exception as e:
        print(f"Error: {e}")  # Missing structured logging
        return False
```

### Log Levels

Use appropriate log levels:

- **DEBUG**: Detailed information, typically for diagnosing problems
- **INFO**: Confirmation that things are working as expected
- **WARNING**: Something unexpected happened, but the application can continue
- **ERROR**: A more serious problem, functionality may be affected
- **CRITICAL**: A very serious error that may prevent the program from continuing

## Exception Handling

### Custom Exceptions

Define a hierarchy of custom exceptions for your application:

```python
# exceptions.py
class BookmarkError(Exception):
    """Base class for bookmark manager exceptions."""
    pass

class NetworkError(BookmarkError):
    """Raised when network operations fail."""
    pass

class DatabaseError(BookmarkError):
    """Raised when database operations fail."""
    pass

class ClassificationError(BookmarkError):
    """Raised when classification fails."""
    pass
```

### Handling Exceptions

✅ **Good:**
```python
from bookmarkmanager.exceptions import NetworkError, DatabaseError

def save_bookmark(url: str) -> int:
    """Save a bookmark to the database.

    Args:
        url: The URL to save

    Returns:
        The ID of the saved bookmark

    Raises:
        NetworkError: If fetching the URL fails
        DatabaseError: If saving to database fails
    """
    try:
        metadata = fetch_url_metadata(url)
    except requests.RequestException as e:
        logger.error("Network error fetching %s: %s", url, str(e))
        raise NetworkError(f"Failed to fetch URL: {url}") from e

    try:
        bookmark_id = db.insert_bookmark(url, metadata)
        return bookmark_id
    except sqlite3.Error as e:
        logger.error("Database error saving bookmark: %s", str(e))
        raise DatabaseError("Failed to save bookmark") from e
```

❌ **Bad:**
```python
def save_bookmark(url: str) -> int:
    """Save a bookmark to the database."""
    try:
        metadata = fetch_url_metadata(url)
        bookmark_id = db.insert_bookmark(url, metadata)
        return bookmark_id
    except Exception as e:  # Too broad exception handling
        print(f"Error: {e}")
        return -1  # Returning magic numbers
```

### Graceful Error Recovery

- Use context managers for resource cleanup
- Implement retry logic for transient failures
- Log stack traces for unexpected errors

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator for functions that might fail transiently."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (NetworkError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(
                            "Failed after %d attempts: %s",
                            max_attempts, str(e)
                        )
                        raise
                    logger.warning(
                        "Attempt %d failed, retrying in %.1f seconds",
                        attempts, delay
                    )
                    time.sleep(delay)
        return wrapper
    return decorator
```

## Documentation

### Documentation as Code

- Keep documentation close to the code
- Update documentation as part of feature development
- Use MkDocs for project documentation



### Documentation Standards

- Document all public APIs
- Include examples in documentation
- Keep documentation up to date with code changes
- Use admonitions for important notes

```
# Command Line Interface

The bookmark manager provides a command line interface for adding, searching, and managing bookmarks.

## Basic Usage


# Add a bookmark
bookmark add https://example.com

# Search bookmarks
bookmark search "machine learning"

# List recent bookmarks
bookmark list --limit 10


!!! note
    All commands support the `--help` flag for more information.

!!! warning
    URLs must include the `http://` or `https://` prefix.
```

## Testing Strategy

### Unit Testing

- Use pytest for test framework
- Aim for high test coverage
- Mock external dependencies

```python
# test_classifier.py
import pytest
from unittest.mock import Mock, patch
from bookmarkmanager.models.classifier import DistilBERTClassifier

@pytest.fixture
def classifier():
    """Create a classifier instance for testing."""
    return DistilBERTClassifier(categories=["Tech", "News", "Personal"])

def test_classify_tech_content(classifier):
    """Test classification of tech content."""
    # Given
    url = "https://example.com/tech-article"
    title = "Python Programming Guide"
    description = "Learn how to program in Python with this guide"

    # When
    result = classifier.classify(url, title, description)

    # Then
    assert "Tech" in result["categories"]
    assert "programming" in result["tags"]

@patch("bookmarkmanager.models.classifier.AutoTokenizer")
@patch("bookmarkmanager.models.classifier.AutoModelForSequenceClassification")
def test_initialization_caches_model(mock_model, mock_tokenizer, tmp_path):
    """Test that model is cached on disk."""
    # Given
    cache_dir = tmp_path / "model_cache"
    cache_dir.mkdir()

    # When
    classifier = DistilBERTClassifier(cache_dir=str(cache_dir))

    # Then
    assert mock_tokenizer.from_pretrained.called
    assert mock_model.from_pretrained.called
    # Verify cache directory was used
    assert "cache_dir" in mock_tokenizer.from_pretrained.call_args[1]
```

### Integration Testing

```python
# test_integration.py
import os
import pytest
import tempfile
from bookmarkmanager.db.database import BookmarkDatabase
from bookmarkmanager.utils.content_processor import extract_metadata
from bookmarkmanager.models.classifier import DistilBERTClassifier

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    db = BookmarkDatabase(path)
    yield db
    os.unlink(path)

def test_end_to_end_bookmark_processing(temp_db):
    """Test the entire bookmark processing pipeline."""
    # Given a test URL
    test_url = "https://python.org"

    # When we process it through the pipeline
    metadata = extract_metadata(test_url)
    classifier = DistilBERTClassifier()
    classification = classifier.classify(
        test_url, metadata["title"], metadata["description"]
    )
    bookmark_id = temp_db.add_bookmark(
        url=test_url,
        title=metadata["title"],
        description=metadata["description"]
    )
    temp_db.add_tags(bookmark_id, classification["tags"])

    # Then we can retrieve it with expected metadata
    bookmark = temp_db.get_bookmark_by_id(bookmark_id)
    assert bookmark is not None
    assert bookmark["url"] == test_url
    assert bookmark["title"] == metadata["title"]

    # And we can find it by tag
    results = temp_db.search_by_tag(classification["tags"][0])
    assert len(results) > 0
    assert any(b["id"] == bookmark_id for b in results)
```

### Test Coverage

- Aim for at least 80% code coverage
- Configure coverage reporting

## Security Best Practices

### Dependency Scanning

- Use tools to scan for vulnerabilities in dependencies
- Update dependencies regularly

### Code Security Scanning

- Use security scanning tools to detect potential vulnerabilities
- Include security checks in CI/CD pipeline


### Input Validation

- Always validate user input
- Use parameterized queries for database operations
- Sanitize data before processing

✅ **Good:**
```python
import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate if string is a proper URL.

    Args:
        url: The URL to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and \
               result.scheme in ['http', 'https']
    except ValueError:
        return False

def add_bookmark(url: str) -> int:
    """Add a bookmark to the database."""
    if not validate_url(url):
        raise ValueError("Invalid URL format")

    # Proceed with validated URL
```

### Additional Best Practices

1. **Type Checking**:
   - Use `mypy` for static type checking
   - Add type stubs for third-party libraries when needed

2. **Profiling and Performance**:
   - Use profiling tools to identify bottlenecks
   - Include performance tests for critical paths

3. **Code Reviews**:
   - Maintain a code review checklist
   - Enforce the "four eyes" principle (at least one reviewer)

4. **Continuous Learning**:
   - Stay updated with Python best practices
   - Share knowledge among team members

5. **User Documentation**:
   - Keep user documentation synchronized with features
   - Include examples for common use cases

This technical specification provides a comprehensive guide for the Bookmark Manager project. By following these guidelines, we ensure a consistent, maintainable, and high-quality codebase.
