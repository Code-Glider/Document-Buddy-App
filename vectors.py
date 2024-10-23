# vectors.py

import os
import base64
from typing import List, Union
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    UnstructuredMarkdownLoader,
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.docstore.document import Document

class EmbeddingsManager:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "vector_db",
    ):
        """
        Initializes the EmbeddingsManager with the specified model and Qdrant settings.

        Args:
            model_name (str): The HuggingFace model name for embeddings.
            device (str): The device to run the model on ('cpu' or 'cuda').
            encode_kwargs (dict): Additional keyword arguments for encoding.
            qdrant_url (str): The URL for the Qdrant instance.
            collection_name (str): The name of the Qdrant collection.
        """
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name

        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

    def _get_loader(self, file_path: str):
        """
        Returns appropriate loader based on file extension.

        Args:
            file_path (str): Path to the file.

        Returns:
            loader: Document loader instance
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return UnstructuredPDFLoader(file_path)
        elif file_extension == '.md':
            return UnstructuredMarkdownLoader(file_path)
        elif file_extension in ['.ts', '.tsx']:
            return TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def create_embeddings(self, file_path: str):
        """
        Processes the document, creates embeddings, and stores them in Qdrant.

        Args:
            file_path (str): The file path to the document.

        Returns:
            str: Success message upon completion.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Load and preprocess the document
        loader = self._get_loader(file_path)
        docs = loader.load()
        if not docs:
            raise ValueError("No documents were loaded from the file.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=250,
            separators=["\n\n", "\n", " ", ""]  # Added more separators for code files
        )
        splits = text_splitter.split_documents(docs)
        if not splits:
            raise ValueError("No text chunks were created from the documents.")

        # Create and store embeddings in Qdrant
        try:
            qdrant = Qdrant.from_documents(
                splits,
                self.embeddings,
                url=self.qdrant_url,
                prefer_grpc=False,
                collection_name=self.collection_name,
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Qdrant: {e}")

        return "✅ Vector DB Successfully Created and Stored in Qdrant!"
