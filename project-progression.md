# Bookmark Manager Project Specification

## 1. Project Overview

A command-line and Telegram-based bookmark management system that automatically categorizes links, supports various import methods, and provides powerful search capabilities. The system uses local LLMs for classification to maintain privacy while enabling efficient bookmark organization.

## 2. Component Objectives

### 2.1 Core Components

- **Database Layer**: Store and manage bookmarks, tags, and relationships in SQLite with full-text search capabilities.
- **Content Processing**: Extract metadata from URLs efficiently using link previews and fallback mechanisms.
- **Classification System**: Categorize bookmarks using local LLMs into user-defined categories.
- **Command Line Interface**: Provide intuitive access to system functionality through structured commands.
- **Telegram Bot**: Enable mobile bookmark capture and retrieval through messaging integration.
- **Importers**: Extract bookmarks from various sources (browser exports, WhatsApp, Telegram, plaintext).

### 2.2 Supporting Components

- **Error Handling**: Provide comprehensive error management across all components.
- **Search Engine**: Enable text-based, tag-based, and semantic search capabilities.
- **Export System**: Generate portable bookmark collections in HTML and JSON formats.
- **Testing Framework**: Ensure component reliability through automated testing.

## 3. Detailed Blueprint

### 3.1 Data Architecture

- **Database Schema**:
  - `bookmarks` table with URL, title, description, and metadata
  - `tags` table with name, category classification
  - `bookmark_tags` junction table for many-to-many relationships
  - Full-text search virtual table for efficient text queries

- **Data Flow**:
  1. Capture input (URL or imported collection)
  2. Extract metadata and content
  3. Classify content
  4. Store in database
  5. Retrieve through queries

### 3.2 User Interaction Flow

- **Adding Bookmarks**:
  1. User submits URL (CLI, Telegram, or import)
  2. System extracts metadata
  3. Classification system assigns tags
  4. Bookmark stored with metadata
  5. User receives confirmation

- **Retrieving Bookmarks**:
  1. User submits search criteria
  2. System queries database
  3. Results formatted according to context
  4. User receives results

### 3.3 Classification System Architecture

- **Tiered Approach**:
  1. Lightweight model for basic classification (DistilBERT)
  2. Rule-based enhancements for common patterns
  3. Optional advanced LLM for complex cases (Phi-3 Mini)
  4. User feedback loop for refinement

## 4. Implementation Plan: Iterative Chunks

### Sprint 1: Foundation
**Objective**: Create a working bookmark storage system with basic CLI

1. **Database Setup**
   - Design and implement SQLite schema
   - Create core CRUD operations
   - Set up indexing and query mechanisms

2. **Basic CLI**
   - Implement add/list commands
   - Create simple formatting
   - Build help system

3. **Simple Content Processing**
   - Implement URL validation
   - Create basic metadata extraction
   - Handle common error cases

### Sprint 2: Classification & Search
**Objective**: Add intelligence to the system

1. **Tag System**
   - Implement tag storage
   - Create many-to-many relationships
   - Build tag management commands

2. **Basic Classification**
   - Set up transformer model
   - Implement simple classification pipeline
   - Create automatic tagging system

3. **Search Capabilities**
   - Implement text search
   - Add tag filtering
   - Create compound queries

### Sprint 3: Import & Export
**Objective**: Enable data migration

1. **Browser Import**
   - Parse HTML bookmark exports
   - Map to internal structure
   - Handle edge cases

2. **Plain Text Import**
   - Extract URLs from text files
   - Process in batch
   - Handle duplicates

3. **Export System**
   - Create HTML export
   - Implement JSON export
   - Ensure portability

### Sprint 4: Telegram Integration
**Objective**: Enable mobile access

1. **Bot Setup**
   - Create Telegram bot
   - Implement authentication
   - Set up command handlers

2. **URL Processing**
   - Detect and extract links
   - Process media messages
   - Handle batch submissions

3. **Search & Retrieval**
   - Format results for mobile
   - Implement pagination
   - Create quick actions

### Sprint 5: Advanced Features
**Objective**: Enhance system capabilities

1. **Advanced Importers**
   - Implement WhatsApp import
   - Create Telegram chat import
   - Build batched processing

2. **Enhanced Classification**
   - Integrate more advanced LLM
   - Implement semantic search
   - Add confidence scores

3. **System Refinement**
   - Performance optimization
   - Error handling improvements
   - User experience enhancements

## 5. Detailed Implementation Steps

### Sprint 1: Foundation

#### Database Setup
1. **Step 1.1**: Design database schema with tables for bookmarks, tags, and relationships
   - **Tasks**:
     - Define table structures, keys, and constraints
     - Document schema with relationships
     - Create SQL initialization scripts

2. **Step 1.2**: Implement SQLite connection management
   - **Tasks**:
     - Create connection handling class
     - Implement connection pooling
     - Add error handling for database operations

3. **Step 1.3**: Build bookmark CRUD operations
   - **Tasks**:
     - Implement create/add bookmark functions
     - Create retrieve operations with filtering
     - Add update and delete functions
     - Write tests for each operation

4. **Step 1.4**: Create indexing and optimization
   - **Tasks**:
     - Add appropriate indexes for common queries
     - Set up full-text search tables
     - Test performance with larger datasets

#### Basic CLI

5. **Step 1.5**: Set up CLI framework
   - **Tasks**:
     - Install and configure Click framework
     - Create command group structure
     - Implement help text and documentation

6. **Step 1.6**: Implement core commands
   - **Tasks**:
     - Create 'add' command with URL validation
     - Implement 'list' command with basic filtering
     - Add 'search' command with simple matching
     - Write tests for each command

7. **Step 1.7**: Build output formatting
   - **Tasks**:
     - Create table output format
     - Implement JSON output option
     - Add simple text output
     - Test with various terminal widths

#### Simple Content Processing

8. **Step 1.8**: Create URL handling
   - **Tasks**:
     - Implement URL validation and normalization
     - Handle common URL formats and edge cases
     - Create tests for URL processing

9. **Step 1.9**: Build metadata extraction
   - **Tasks**:
     - Implement basic HTTP fetching
     - Create HTML title and description extraction
     - Add error handling for inaccessible sites
     - Test with various website types

10. **Step 1.10**: Add storage integration
    - **Tasks**:
      - Connect URL processing to database storage
      - Implement duplicate detection
      - Add batch processing capability
      - Write integration tests

### Sprint 2: Classification & Search

#### Tag System

11. **Step 2.1**: Implement tag storage
    - **Tasks**:
      - Create tag management functions
      - Implement tag normalization
      - Add bulk tag operations
      - Test tag creation and retrieval

12. **Step 2.2**: Build tag relationships
    - **Tasks**:
      - Implement tag-bookmark associations
      - Create functions to add/remove tags
      - Build tag recommendation system
      - Test relationship management

13. **Step 2.3**: Create tag commands
    - **Tasks**:
      - Add CLI commands for tag management
      - Implement tag filtering in search
      - Create tag statistics functions
      - Test tag command functionality

#### Basic Classification

14. **Step 2.4**: Set up classification environment
    - **Tasks**:
      - Install and configure transformer libraries
      - Create model loading and caching
      - Set up classification abstraction layer
      - Test environment setup

15. **Step 2.5**: Implement basic classifier
    - **Tasks**:
      - Create text preprocessing pipeline
      - Implement classification prediction
      - Add confidence scoring
      - Test classification accuracy

16. **Step 2.6**: Connect classification to bookmarks
    - **Tasks**:
      - Integrate classification during bookmark addition
      - Create automatic tagging based on classification
      - Add manual override capabilities
      - Write integration tests

#### Search Capabilities

17. **Step 2.7**: Implement basic search
    - **Tasks**:
      - Create text-based search function
      - Implement relevance sorting
      - Add result limiting and pagination
      - Test search accuracy

18. **Step 2.8**: Add advanced filtering
    - **Tasks**:
      - Implement tag-based filtering
      - Add date range filtering
      - Create combined search filters
      - Test filter combinations

19. **Step 2.9**: Enhance CLI search commands
    - **Tasks**:
      - Update CLI with advanced search options
      - Implement search result formatting
      - Add sorting options
      - Test command usability

### Sprint 3: Import & Export

#### Browser Import

20. **Step 3.1**: Create HTML parser
    - **Tasks**:
      - Implement browser bookmark HTML parsing
      - Extract bookmark folders as categories
      - Handle nested structures
      - Test with exports from major browsers

21. **Step 3.2**: Build import pipeline
    - **Tasks**:
      - Create batch processing for imports
      - Implement duplicate detection
      - Add progress reporting
      - Test with large import files

22. **Step 3.3**: Add CLI import command
    - **Tasks**:
      - Create import command with options
      - Implement source selection
      - Add reporting of import results
      - Test command functionality

#### Plain Text Import

23. **Step 3.4**: Implement text extraction
    - **Tasks**:
      - Create URL extraction from plain text
      - Implement context detection for categorization
      - Add batch processing
      - Test with various text formats

24. **Step 3.5**: Build metadata enhancement
    - **Tasks**:
      - Create pipeline to fetch missing metadata
      - Implement parallel processing
      - Add error handling for failed fetches
      - Test with various link types

25. **Step 3.6**: Connect to CLI
    - **Tasks**:
      - Add plain text import to CLI
      - Implement format autodetection
      - Create reporting for text imports
      - Test usability

#### Export System

26. **Step 3.7**: Create HTML export
    - **Tasks**:
      - Implement HTML bookmark format generation
      - Add folder structure based on categories
      - Create template system for customization
      - Test with browser import compatibility

27. **Step 3.8**: Build JSON export
    - **Tasks**:
      - Implement JSON serialization
      - Add filtering options for export
      - Create pretty and compact formats
      - Test data integrity

28. **Step 3.9**: Add export commands
    - **Tasks**:
      - Create export CLI commands
      - Implement format selection
      - Add output file handling
      - Test export functionality

### Sprint 4: Telegram Integration

#### Bot Setup

29. **Step 4.1**: Create Telegram bot
    - **Tasks**:
      - Register bot with BotFather
      - Implement basic message handling
      - Create command structure
      - Test bot responsiveness

30. **Step 4.2**: Implement authentication
    - **Tasks**:
      - Create user authentication system
      - Implement privacy controls
      - Add user-specific data handling
      - Test security measures

31. **Step 4.3**: Build command handlers
    - **Tasks**:
      - Implement core command parsing
      - Create help system
      - Add error handling
      - Test command functionality

#### URL Processing

32. **Step 4.4**: Create link detection
    - **Tasks**:
      - Implement URL extraction from messages
      - Create auto-detection for plain URLs
      - Handle forwarded messages
      - Test detection accuracy

33. **Step 4.5**: Build processing pipeline
    - **Tasks**:
      - Connect URL detection to bookmark system
      - Implement asynchronous processing
      - Add status feedback
      - Test end-to-end functionality

34. **Step 4.6**: Add batch handling
    - **Tasks**:
      - Implement multiple URL processing
      - Create progress reporting
      - Add summary generation
      - Test with various message types

#### Search & Retrieval

35. **Step 4.7**: Implement search commands
    - **Tasks**:
      - Create search command parsing
      - Implement query processing
      - Connect to search engine
      - Test search accuracy

36. **Step 4.8**: Build result formatting
    - **Tasks**:
      - Create mobile-friendly result format
      - Implement pagination
      - Add inline buttons for actions
      - Test on mobile devices

37. **Step 4.9**: Add quick actions
    - **Tasks**:
      - Implement inline tag editing
      - Create bookmark sharing
      - Add delete functionality
      - Test user interaction flow

### Sprint 5: Advanced Features

#### Advanced Importers

38. **Step 5.1**: Implement WhatsApp import
    - **Tasks**:
      - Create WhatsApp chat export parser
      - Extract URLs and context
      - Handle message formatting
      - Test with various chat exports

39. **Step 5.2**: Build Telegram chat import
    - **Tasks**:
      - Implement Telegram export JSON parsing
      - Extract links with metadata
      - Handle media captions
      - Test with different export formats

40. **Step 5.3**: Create unified import system
    - **Tasks**:
      - Build common import interface
      - Implement format auto-detection
      - Create import reporting system
      - Test with mixed source imports

#### Enhanced Classification

41. **Step 5.4**: Integrate advanced LLM
    - **Tasks**:
      - Set up Phi-3 Mini or similar model
      - Implement quantization for efficiency
      - Create model caching system
      - Test classification accuracy

42. **Step 5.5**: Implement semantic search
    - **Tasks**:
      - Create embedding generation for bookmarks
      - Implement vector similarity search
      - Add hybrid search capabilities
      - Test semantic relevance

43. **Step 5.6**: Add confidence scoring
    - **Tasks**:
      - Implement classification confidence metrics
      - Create threshold-based tag application
      - Add user feedback loop
      - Test classification quality

#### System Refinement

44. **Step 5.7**: Performance optimization
    - **Tasks**:
      - Profile system performance
      - Optimize database queries
      - Implement caching where appropriate
      - Test with larger datasets

45. **Step 5.8**: Error handling improvements
    - **Tasks**:
      - Review and enhance error handling
      - Implement logging system
      - Create user-friendly error messages
      - Test error recovery

46. **Step 5.9**: User experience enhancements
    - **Tasks**:
      - Review and refine CLI interface
      - Enhance Telegram interaction flow
      - Add configuration management
      - Conduct usability testing

## 6. Development Approach

### 6.1 Testing Strategy

- **Unit Testing**: Test individual components in isolation
- **Integration Testing**: Verify components work together
- **End-to-End Testing**: Validate complete user workflows
- **Performance Testing**: Ensure system handles larger datasets efficiently

### 6.2 Development Workflow

1. **Feature Branch Development**:
   - Create branch for each step
   - Implement tasks with tests
   - Review and refine
   - Merge when complete

2. **Continuous Integration**:
   - Run tests automatically on push
   - Enforce code quality standards
   - Check for regression issues

3. **Iterative Releases**:
   - Create working system at end of each sprint
   - Get feedback early and often
   - Adjust plan based on learnings

### 6.3 Documentation

- **Code Documentation**: Document classes, functions, and methods
- **User Documentation**: Create usage guides for CLI and Telegram
- **System Architecture**: Document component interactions and data flow

## 7. Resource Requirements

- **Development Environment**: Python 3.10+, SQLite
- **Libraries**: Click, Transformers, python-telegram-bot, BeautifulSoup, Requests
- **Models**: DistilBERT (basic), Phi-3 Mini or Gemma 2B (advanced)
- **Computing Resources**: Local development with at least 8GB RAM, 4 cores

This specification provides a comprehensive, step-by-step blueprint for building the Bookmark Manager, with carefully sized implementation steps that balance testability with meaningful progress.