# vectors.py

import os
import base64
import json
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Union, Dict
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
    CSVLoader,
    JSONLoader,
    UnstructuredXMLLoader,
    BSHTMLLoader,  # Added HTML Loader
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,  # Added for code-specific splitting
    HTMLHeaderTextSplitter  # Added for HTML header-based splitting
)
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

    def _json_extract_func(self, data: Dict) -> str:
        """
        Extracts text content from JSON data.
        """
        text_items = []
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                text_items.append(f"{key}: {value}")
            elif isinstance(value, (dict, list)):
                text_items.append(f"{key}: {json.dumps(value, indent=2)}")
        return "\n".join(text_items)

    def _get_loader(self, file_path: str):
        """
        Returns appropriate loader based on file extension.
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return UnstructuredPDFLoader(file_path)
        elif file_extension == '.md':
            return UnstructuredMarkdownLoader(file_path)
        elif file_extension in ['.ts', '.tsx']:
            return TextLoader(file_path)
        elif file_extension == '.csv':
            return CSVLoader(
                file_path,
                source_column="source" if "source" in self._get_csv_columns(file_path) else None,
                encoding="utf-8"
            )
        elif file_extension == '.json':
            return JSONLoader(
                file_path=file_path,
                jq_schema=".",
                text_content=False,
                json_lines=False,
                extract_func=self._json_extract_func
            )
        elif file_extension == '.xml':
            return UnstructuredXMLLoader(file_path)
        elif file_extension == '.html':
            return BSHTMLLoader(file_path)
        elif file_extension in ['.css', '.scss']:
            return TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def _get_css_splitter(self) -> RecursiveCharacterTextSplitter:
        """
        Returns a text splitter configured for CSS/SCSS files.
        """
        return RecursiveCharacterTextSplitter.from_language(
            language=Language.CSS,
            chunk_size=800,
            chunk_overlap=100,
        )

    def _get_html_splitter(self) -> RecursiveCharacterTextSplitter:
        """
        Returns a text splitter configured for HTML files.
        """
        headers_to_split_on = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
            ("h4", "Header 4"),
        ]
        return HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    def _get_chunk_settings(self, file_path: str) -> Dict[str, int]:
        """
        Returns appropriate chunk settings based on file type.
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        settings = {
            '.csv': {'chunk_size': 500, 'chunk_overlap': 50},
            '.json': {'chunk_size': 800, 'chunk_overlap': 100},
            '.xml': {'chunk_size': 800, 'chunk_overlap': 100},
            '.html': {'chunk_size': 1000, 'chunk_overlap': 200},
            '.css': {'chunk_size': 800, 'chunk_overlap': 100},
            '.scss': {'chunk_size': 800, 'chunk_overlap': 100},
            'default': {'chunk_size': 1000, 'chunk_overlap': 250}
        }
        return settings.get(file_extension, settings['default'])

    def _get_text_splitter(self, file_path: str):
        """
        Returns appropriate text splitter based on file type.
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.css', '.scss']:
            return self._get_css_splitter()
        elif file_extension == '.html':
            return self._get_html_splitter()
        else:
            chunk_settings = self._get_chunk_settings(file_path)
            return RecursiveCharacterTextSplitter(
                chunk_size=chunk_settings['chunk_size'],
                chunk_overlap=chunk_settings['chunk_overlap'],
                separators=["\n\n", "\n", " ", ""]
            )

    def create_embeddings(self, file_path: str):
        """
        Processes the document, creates embeddings, and stores them in Qdrant.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Load and preprocess the document
        loader = self._get_loader(file_path)
        docs = loader.load()
        if not docs:
            raise ValueError("No documents were loaded from the file.")

        # Get appropriate text splitter
        text_splitter = self._get_text_splitter(file_path)
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
