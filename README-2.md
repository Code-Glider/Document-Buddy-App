tutorial link : https://www.youtube.com/watch?v=7hnZ6SFnXXA
tutorial description :
I've created a tutorial video showcasing a real-time Retrieval Augmented Generation (RAG) app built using Qdrant, LLaMA 3.2, BGE embeddings, and unstructured. This app efficiently retrieves and generates contextual information by combining powerful vector search with LLaMA's capabilities, making it ideal for applications like document search and question-answering systems. The complete code is available on GitHub for you to explore.

📄 Document Buddy App
Document Buddy App

Document Buddy App is a powerful Streamlit-based application designed to simplify document management. Upload your PDF documents, create embeddings for efficient retrieval, and interact with your documents through an intelligent chatbot interface. 🚀

🛠️ Features
📂 Upload Documents: Easily upload and preview your PDF documents within the app.
🧠 Create Embeddings: Generate embeddings for your documents to enable efficient search and retrieval.
🤖 Chatbot Interface: Interact with your documents using a smart chatbot that leverages the created embeddings.
📧 Contact: Get in touch with the developer or contribute to the project on GitHub.
🌟 User-Friendly Interface: Enjoy a sleek and intuitive UI with emojis and responsive design for enhanced user experience.
🖥️ Tech Stack
The Document Buddy App leverages a combination of cutting-edge technologies to deliver a seamless and efficient user experience. Here's a breakdown of the technologies and tools used:

LangChain: Utilized as the orchestration framework to manage the flow between different components, including embeddings creation, vector storage, and chatbot interactions.

Unstructured: Employed for robust PDF processing, enabling the extraction and preprocessing of text from uploaded PDF documents.

BGE Embeddings from HuggingFace: Used to generate high-quality embeddings for the processed documents, facilitating effective semantic search and retrieval.

Qdrant: A vector database running locally via Docker, responsible for storing and managing the generated embeddings for fast and scalable retrieval.

LLaMA 3.2 via Ollama: Integrated as the local language model to power the chatbot, providing intelligent and context-aware responses based on the document embeddings.

Streamlit: The core framework for building the interactive web application, offering an intuitive interface for users to upload documents, create embeddings, and interact with the chatbot.

📁 Directory Structure
document_buddy_app/

│── logo.png
├── new.py
├── vectors.py
├── chatbot.py
├── requirements.txt





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
ollama run minicpm-v
ollama pull bge-m3
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
