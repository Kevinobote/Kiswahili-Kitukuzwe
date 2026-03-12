# Project Structure

```
Deployed/
├── frontend/                    # Web interface
│   ├── static/
│   │   ├── app.js              # Frontend JavaScript with PhD features
│   │   └── style.css           # Professional styling
│   └── index.html              # Main web page
│
├── models/                      # ML Pipeline
│   ├── __init__.py
│   ├── pipeline_manager.py     # Main pipeline orchestrator
│   └── chunking_utils.py       # Audio/text chunking utilities
│
├── schemas/                     # API Models
│   ├── __init__.py
│   └── response_models.py      # Pydantic response schemas
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md         # System architecture
│   ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│   ├── ENVIRONMENT.md          # Environment setup
│   ├── FRONTEND_DOCUMENTATION.md
│   ├── FRONTEND_IMPROVEMENTS.md
│   ├── QUICK_REFERENCE.md
│   └── README_TESTING.md
│
├── config/                      # Configuration files (empty)
├── tests/                       # Test files (empty)
├── logs/                        # Application logs (gitignored)
│
├── main.py                      # FastAPI application
├── modal_app.py                 # Modal deployment config
├── requirements.txt             # Python dependencies
├── setup_env.sh                 # Environment setup script
├── deploy_modal.sh              # Modal deployment script
│
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── DEPLOYMENT_COMPARISON.md     # Deployment options comparison
├── MODAL_DEPLOYMENT.md          # Modal deployment guide
├── MODAL_QUICK_START.md         # Quick start for Modal
└── SERVER_DEPLOYMENT.md         # Server deployment guide
```

## Key Files

### Core Application
- **main.py**: FastAPI backend with all endpoints
- **modal_app.py**: Serverless deployment configuration
- **requirements.txt**: All Python dependencies

### ML Pipeline
- **models/pipeline_manager.py**: AudioProcessingPipeline class
- **models/chunking_utils.py**: AudioChunker, TextChunker, ResultAggregator

### Frontend
- **frontend/index.html**: PhD-level UI with metrics dashboard
- **frontend/static/app.js**: Advanced features (Chart.js, export, drag-drop)
- **frontend/static/style.css**: Professional styling

### Deployment
- **deploy_modal.sh**: One-command Modal deployment
- **setup_env.sh**: Local environment setup

## Ignored Files (not in Git)
- `sema-deployed/` - Virtual environment
- `logs/` - Application logs
- `__pycache__/` - Python cache
- `.cache/` - Model cache
