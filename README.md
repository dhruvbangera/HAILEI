# HAILEI - Instructional Design Layer

A comprehensive educational technology framework that enables collaborative course development through intelligent agent coordination.

## Project Structure

```
HAILEI/
├── agents/                     # AI Agent implementations
│   ├── streamlit/             # Streamlit-based agent interfaces
│   │   ├── CAuthAi.py         # Course Authoring Agent
│   │   ├── EthosAi.py         # Ethical Oversight Agent
│   │   ├── IPDAi.py           # Instructional Planning & Design Agent
│   │   ├── SearchAi.py        # Semantic Search & Enrichment Agent
│   │   ├── TFDAi.py           # Technical & Functional Design Agent
│   │   └── EditorAi.py        # Content Review & Enhancement Agent
│   ├── core/                  # Core agent logic and APIs
│   └── utils/                 # Shared utilities and helpers
├── workflows/                 # Orchestration workflows
│   └── n8n/                   # n8n workflow configurations
│       └── HAILEI_n8n_workflow.json
├── docs/                      # Documentation
│   ├── architecture/          # System architecture docs
│   └── user-guides/          # User documentation
├── tests/                     # Test suites
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── config/                   # Configuration files
├── data/                     # Data files and samples
├── requirements/             # Dependencies and requirements
└── README.md                 # This file
```

## Core Components

### 🤖 Intelligent Agents

1. **IPDAi** - Instructional Planning and Design Agent
2. **CAuthAi** - Course Authoring Agent  
3. **TFDAi** - Technical & Functional Design Agent
4. **EditorAi** - Content Review & Enhancement Agent
5. **EthosAi** - Ethical Oversight Agent
6. **SearchAi** - Semantic Search & Enrichment Agent

### 🎯 Pedagogical Frameworks

- **KDKA Model**: Knowledge, Delivery, Context, Assessment
- **PRRR Model**: Personal, Relatable, Relative, Real-world
- **Revised Bloom's Taxonomy**: Cognitive progression framework
- **TILT Framework**: Transparency in Learning and Teaching

## Quick Start

### Prerequisites
- Python 3.8+
- Streamlit
- n8n (for orchestration)

### Running Individual Agents
```bash
cd agents/streamlit
streamlit run IPDAi.py
```

### Setting up n8n Workflow
1. Import `workflows/n8n/HAILEI_n8n_workflow.json` into n8n
2. Configure OpenAI API keys
3. Set up webhook triggers

## Development Status

- ✅ Core architecture defined
- ✅ Agent specifications complete
- 🚧 Streamlit implementations (in progress)
- ⏳ n8n workflow integration (pending)
- ⏳ Testing framework (pending)

## License

Educational use - See LICENSE file for details.