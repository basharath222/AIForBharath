# IdeaTechTrace AI - Design Document

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Streamlit Frontend)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Orchestration Layer                        │
│                  (FastAPI + LangChain)                       │
└─────┬──────────┬──────────┬──────────┬─────────────────────┘
      │          │          │          │
      ▼          ▼          ▼          ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│ Code    │ │ Doc    │ │ Query  │ │ Visualization│
│ Indexer │ │ Sync   │ │ Engine │ │ Generator    │
└────┬────┘ └───┬────┘ └───┬────┘ └──────┬───────┘
     │          │          │             │
     └──────────┴──────────┴─────────────┘
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
┌─────────┐  ┌────────────┐  ┌──────────┐
│ Vector  │  │   Amazon   │  │ Mermaid  │
│   DB    │  │  Bedrock   │  │   .js    │
│(Kendra/ │  │  (Claude)  │  │ Renderer │
│Pinecone)│  │            │  │          │
└─────────┘  └────────────┘  └──────────┘
```
 
## Component Design

### 1. Frontend Layer (Streamlit)

#### 1.1 Main Application (`app.py`)
```python
# Core UI components:
- Session state management
- Layout configuration (split-screen)
- User authentication (if needed)
- Theme management
```

**Key Pages:**
- Home/Dashboard
- Code Explorer
- Interactive Tutor
- Visualization Studio
- Sprint Summary

#### 1.2 UI Components

**Code Viewer Component**
- Syntax highlighting
- Line number display
- Code selection handler
- File tree navigation

**Chat Interface Component**
- Message history
- Input field with autocomplete
- Quick action buttons
- Skill level selector

**Visualization Panel Component**
- Diagram renderer (Mermaid.js)
- Export controls
- Zoom/pan functionality
- Diagram type selector

### 2. Orchestration Layer (FastAPI + LangChain)

#### 2.1 API Endpoints (`api/main.py`)

```python
POST /api/ingest
    - Accepts: repo_url or local_path
    - Returns: ingestion_id, status
    
POST /api/query
    - Accepts: question, context, skill_level
    - Returns: answer, sources, confidence
    
POST /api/visualize
    - Accepts: code_block, diagram_type
    - Returns: mermaid_code, svg_url
    
GET /api/summary
    - Accepts: session_id
    - Returns: summary_markdown
    
POST /api/doc-sync
    - Accepts: doc_url or pdf_file
    - Returns: sync_status, doc_id
```

#### 2.2 LangChain Pipeline (`core/rag_pipeline.py`)

```python
class RAGPipeline:
    - DocumentLoader: Load and parse code files
    - TextSplitter: Chunk documents intelligently
    - EmbeddingGenerator: Create vector embeddings
    - VectorStore: Store and retrieve embeddings
    - RetrievalChain: Query and retrieve context
    - ResponseGenerator: Generate answers with citations
```

### 3. Core Modules

#### 3.1 Code Indexer (`core/indexer.py`)

**Responsibilities:**
- Parse project structure
- Extract code metadata (functions, classes, imports)
- Generate embeddings for code blocks
- Store in vector database

**Key Classes:**
```python
class CodeIndexer:
    def index_repository(repo_path: str) -> IndexResult
    def index_file(file_path: str) -> FileIndex
    def extract_metadata(code: str, language: str) -> Metadata
    def generate_embeddings(chunks: List[str]) -> List[Vector]
```

#### 3.2 Documentation Sync (`core/doc_sync.py`)

**Responsibilities:**
- Fetch documentation from URLs
- Parse PDF documents
- Extract structured content
- Update vector database

**Key Classes:**
```python
class DocSyncManager:
    def sync_from_url(url: str) -> SyncResult
    def sync_from_pdf(pdf_path: str) -> SyncResult
    def parse_documentation(content: str) -> List[DocChunk]
    def update_vector_store(chunks: List[DocChunk]) -> bool
```

#### 3.3 Query Engine (`core/query_engine.py`)

**Responsibilities:**
- Process user queries
- Retrieve relevant context
- Generate responses with citations
- Apply hallucination guard

**Key Classes:**
```python
class QueryEngine:
    def process_query(query: str, context: Context) -> Response
    def retrieve_context(query: str, top_k: int) -> List[Document]
    def generate_response(query: str, context: List[Document]) -> str
    def apply_hallucination_guard(response: str) -> ValidationResult
```

#### 3.4 Visualization Generator (`core/visualizer.py`)

**Responsibilities:**
- Analyze code structure
- Generate Mermaid.js diagrams
- Create use-case diagrams
- Produce architecture diagrams

**Key Classes:**
```python
class VisualizationGenerator:
    def generate_flowchart(code: str) -> str  # Returns Mermaid code
    def generate_use_case_diagram(folder: str) -> str
    def generate_architecture_diagram(project: str) -> str
    def code_to_mermaid(ast_tree: AST) -> str
```

#### 3.5 Hallucination Guard (`core/hallucination_guard.py`)

**Responsibilities:**
- Cross-reference AI responses with documentation
- Calculate confidence scores
- Flag uncertain information
- Provide source citations

**Key Classes:**
```python
class HallucinationGuard:
    def verify_response(response: str, sources: List[Doc]) -> ValidationResult
    def calculate_confidence(response: str, context: str) -> float
    def extract_claims(response: str) -> List[Claim]
    def verify_claim(claim: Claim, sources: List[Doc]) -> bool
```

#### 3.6 Sprint Summarizer (`core/summarizer.py`)

**Responsibilities:**
- Track session activities
- Analyze code changes
- Generate learning summaries
- Export reports

**Key Classes:**
```python
class SprintSummarizer:
    def track_activity(event: ActivityEvent) -> None
    def generate_summary(session_id: str) -> Summary
    def analyze_changes(files: List[str]) -> ChangeAnalysis
    def export_markdown(summary: Summary) -> str
```

### 4. Data Layer

#### 4.1 Vector Database Schema

**Collections:**

**code_embeddings**
```json
{
  "id": "uuid",
  "project_id": "string",
  "file_path": "string",
  "chunk_text": "string",
  "embedding": [float],
  "metadata": {
    "language": "string",
    "function_name": "string",
    "class_name": "string",
    "line_start": int,
    "line_end": int
  },
  "timestamp": "datetime"
}
```

**doc_embeddings**
```json
{
  "id": "uuid",
  "doc_source": "string",
  "doc_type": "string",
  "chunk_text": "string",
  "embedding": [float],
  "metadata": {
    "title": "string",
    "section": "string",
    "url": "string",
    "version": "string"
  },
  "timestamp": "datetime"
}
```

#### 4.2 Session Storage (SQLite/PostgreSQL)

**Tables:**

**projects**
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    path TEXT,
    repo_url TEXT,
    indexed_at TIMESTAMP,
    file_count INTEGER,
    status VARCHAR(50)
);
```

**sessions**
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    user_id VARCHAR(255),
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    query_count INTEGER
);
```

**queries**
```sql
CREATE TABLE queries (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    question TEXT,
    answer TEXT,
    confidence FLOAT,
    skill_level VARCHAR(50),
    created_at TIMESTAMP
);
```

**documentation**
```sql
CREATE TABLE documentation (
    id UUID PRIMARY KEY,
    source_url TEXT,
    doc_type VARCHAR(50),
    title VARCHAR(255),
    synced_at TIMESTAMP,
    chunk_count INTEGER,
    status VARCHAR(50)
);
```

## Process Flows

### Flow 1: Project Ingestion

```
User Input (Repo URL/Local Path)
    ↓
Validate Input
    ↓
Clone/Access Repository
    ↓
Scan File Structure
    ↓
Parse Code Files (by language)
    ↓
Extract Metadata (AST parsing)
    ↓
Chunk Code Intelligently
    ↓
Generate Embeddings (Bedrock)
    ↓
Store in Vector DB
    ↓
Update Project Status
    ↓
Return Success + Stats
```

### Flow 2: Interactive Query

```
User Question + Optional Code Selection
    ↓
Determine Skill Level
    ↓
Preprocess Query (extract intent)
    ↓
Retrieve Relevant Code Context (Vector Search)
    ↓
Retrieve Relevant Documentation (Vector Search)
    ↓
Construct Prompt with Context
    ↓
Send to Amazon Bedrock (Claude 3)
    ↓
Receive Response
    ↓
Apply Hallucination Guard
    ↓
Format Response with Citations
    ↓
Display to User
    ↓
Log Query for Session Summary
```

### Flow 3: Visualization Generation

```
User Selects Code Block/Folder
    ↓
Determine Diagram Type
    ↓
Parse Code Structure (AST)
    ↓
Extract Relationships
    ↓
Generate Mermaid.js Syntax
    ↓
Render Diagram
    ↓
Display with Export Options
```

### Flow 4: Documentation Sync

```
User Provides Doc URL/PDF
    ↓
Fetch/Load Document
    ↓
Parse Content (HTML/PDF parser)
    ↓
Extract Structured Sections
    ↓
Chunk Documentation
    ↓
Generate Embeddings
    ↓
Store in Vector DB
    ↓
Update Doc Registry
    ↓
Notify User of Completion
```

## Technology Stack Details

### Frontend
- **Streamlit**: Rapid UI development
- **Mermaid.js**: Diagram rendering
- **Plotly**: Interactive charts (for metrics)
- **Streamlit-Ace**: Code editor component

### Backend
- **FastAPI**: REST API framework
- **LangChain**: RAG orchestration
- **Python 3.9+**: Core language

### AI/ML
- **Amazon Bedrock**: LLM provider
  - Claude 3 Sonnet: Primary model
  - Titan Embeddings: Vector generation
- **LangChain**: Framework for RAG

### Data Storage
- **Amazon Kendra** (Primary): Enterprise vector search
- **Pinecone** (Alternative): Vector database
- **SQLite/PostgreSQL**: Metadata storage
- **Redis**: Caching layer (optional)

### Code Analysis
- **Tree-sitter**: Multi-language parsing
- **Pygments**: Syntax highlighting
- **AST**: Python code analysis

### Documentation Processing
- **BeautifulSoup4**: HTML parsing
- **PyPDF2/pdfplumber**: PDF extraction
- **Markdown**: Documentation format

## Security Considerations

### API Key Management
- Store AWS credentials in environment variables
- Use AWS Secrets Manager for production
- Implement key rotation policies

### Code Privacy
- Local-first processing option
- Encrypted vector storage
- No code transmission without consent
- Clear data retention policies

### Access Control
- User authentication (optional for v1.0)
- Project-level permissions
- Rate limiting on API endpoints

## Performance Optimization

### Caching Strategy
- Cache frequently accessed embeddings
- Cache LLM responses for identical queries
- Implement TTL for cached data

### Batch Processing
- Batch embedding generation
- Parallel file processing during ingestion
- Async API calls to Bedrock

### Resource Management
- Limit concurrent Bedrock requests
- Implement request queuing
- Monitor token usage

## Error Handling

### Graceful Degradation
- Fallback to cached responses when API unavailable
- Provide partial results when possible
- Clear error messages to users

### Retry Logic
- Exponential backoff for API failures
- Maximum retry attempts: 3
- Circuit breaker pattern for external services

## Monitoring & Logging

### Metrics to Track
- Query response times
- Embedding generation times
- API success/failure rates
- User satisfaction scores
- Hallucination detection rate

### Logging Strategy
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Separate logs for user actions and system events
- PII redaction in logs

## Deployment Architecture

### Development
- Local Streamlit server
- SQLite database
- Mock AWS services (optional)

### Production
- Containerized deployment (Docker)
- Load balancer for API
- Managed database (RDS/Aurora)
- CDN for static assets
- Auto-scaling based on load

## Testing Strategy

### Unit Tests
- Test individual components
- Mock external dependencies
- Coverage target: 80%

### Integration Tests
- Test RAG pipeline end-to-end
- Test API endpoints
- Test database operations

### User Acceptance Tests
- Test with real codebases
- Validate diagram accuracy
- Verify hallucination guard effectiveness

## Future Architecture Considerations

- Microservices architecture for scalability
- Multi-tenant support
- Real-time collaboration features
- Plugin system for extensibility
- Custom model fine-tuning pipeline
