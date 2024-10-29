# Document Buddy App Complete Setup Guide

## Prerequisites Installation
1. **Install Required Software**
```powershell
# Download and install these in order:
- Node.js LTS from https://nodejs.org/
- GitHub Desktop from https://desktop.github.com/
- Docker Desktop from https://www.docker.com/products/docker-desktop/
```

## Environment Setup

1. **Set Environment Variables**
```powershell
# Add to Windows System Variables
Variable name: NODE_HOME
Variable value: C:\Program Files\nodejs

# Add to Path
C:\Program Files\nodejs
C:\Program Files\nodejs\node_modules
```

2. **Clone Repository**
```powershell
# Using GitHub Desktop
- Click "File" > "Clone Repository"
- URL: https://github.com/AIAnytime/Document-Buddy-App.git
- Local path: I:\projects\Document-Buddy-App
```

## Docker and Database Setup

1. **Configure Qdrant with Docker**
```powershell
# Create local storage directory
mkdir I:\projects\Document-Buddy-App\qdrant-storage

# Create Docker volume
docker volume create qdrant_storage

# Run Qdrant container
docker run -d `
  --name qdrant `
  -p 6333:6333 `
  -v qdrant_storage:/qdrant/storage `
  -v I:\projects\Document-Buddy-App\qdrant-storage:/qdrant/local_storage `
  qdrant/qdrant

# Verify setup
docker volume ls
docker ps
```

## Application Setup

1. **Python Environment**
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Install Ollama Models**
```powershell
# Start Ollama
ollama serve

# Install required models
ollama pull minicpm-vlatest
ollama pull bge-small-en
```

3. **Configure Application Settings**
- Theme: Dark
- Chat Model Provider: Ollama
- Chat Model: minicpm-vlatest
- Embedding Model Provider: Local
- Embedding Model: BGE Small
- Ollama API URL: http://localhost:11434

## Start Application

1. **Run Application**
```powershell
# Start application
cd I:\projects\Document-Buddy-App
streamlit run new.py
```

## Verify Installation

1. **Check Services**
- Qdrant running on http://localhost:6333
- Ollama running on http://localhost:11434
- Application running on http://localhost:8501

2. **Test Functionality**
- Upload a document
- Create embeddings
- Test chat interface

## Common Issues and Solutions

1. **Connection Issues**
- Verify Ollama API URL is correct (http://localhost:11434)
- Ensure no typos (use number '1' not letter 'l')
- Check if all services are running

2. **Docker Issues**
- Verify volumes are created
- Check container logs
- Ensure ports aren't in use

3. **Application Issues**
- Keep Ollama running in background
- Verify all models are installed
- Check console for error messages

## Directory Structure
```
I:\projects\Document-Buddy-App\
├── venv\
├── qdrant-storage\
├── new.py
├── vectors.py
├── chatbot.py
├── requirements.txt
└── logo.png
```

Remember to save all settings and restart services if needed.

Citations:
[1] https://pplx-res.cloudinary.com/image/upload/v1729963489/user_uploads/lrfrxehap/image.jpg
[2] https://pplx-res.cloudinary.com/image/upload/v1729967352/user_uploads/qsbptbliw/image.jpg
