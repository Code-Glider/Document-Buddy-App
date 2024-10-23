import os
from typing import List, Dict
from langchain_community.document_loaders import UnstructuredFileLoader
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
        Returns UnstructuredFileLoader that handles all file types.

        Args:
            file_path (str): Path to the file.

        Returns:
            UnstructuredFileLoader: Document loader instance
        """
        return UnstructuredFileLoader(
            file_path,
            mode="elements",
            strategy="fast"
        )

    def _get_chunk_settings(self, file_path: str) -> Dict[str, int]:
        """
        Returns appropriate chunk settings based on file type.

        Args:
            file_path (str): Path to the file.

        Returns:
            Dict[str, int]: Dictionary containing chunk size and overlap settings
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        settings = {
            # Text files and documentation
            '.txt': {'chunk_size': 1000, 'chunk_overlap': 200},
            '.md': {'chunk_size': 1000, 'chunk_overlap': 200},
            '.pdf': {'chunk_size': 1000, 'chunk_overlap': 200},
            '.doc': {'chunk_size': 1000, 'chunk_overlap': 200},
            '.docx': {'chunk_size': 1000, 'chunk_overlap': 200},
            
            # Code files
            '.py': {'chunk_size': 800, 'chunk_overlap': 150},
            '.js': {'chunk_size': 800, 'chunk_overlap': 150},
            '.jsx': {'chunk_size': 800, 'chunk_overlap': 150},
            '.ts': {'chunk_size': 800, 'chunk_overlap': 150},
            '.tsx': {'chunk_size': 800, 'chunk_overlap': 150},
            '.css': {'chunk_size': 600, 'chunk_overlap': 100},
            '.scss': {'chunk_size': 600, 'chunk_overlap': 100},
            '.html': {'chunk_size': 800, 'chunk_overlap': 150},
            
            # Data files
            '.json': {'chunk_size': 500, 'chunk_overlap': 100},
            '.xml': {'chunk_size': 500, 'chunk_overlap': 100},
            '.csv': {'chunk_size': 500, 'chunk_overlap': 50},
            
            # Default settings
            'default': {'chunk_size': 1000, 'chunk_overlap': 200}
        }
        
        return settings.get(file_extension, settings['default'])

    def create_embeddings(self, file_path: str):
        """
        Processes the document, creates embeddings, and stores them in Qdrant.

        Args:
            file_path (str): The file path to the document.

        Returns:
            str: Success message upon completion.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If no documents are loaded or no chunks are created.
            ConnectionError: If connection to Qdrant fails.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Load document
        try:
            loader = self._get_loader(file_path)
            docs = loader.load()
            if not docs:
                raise ValueError("No documents were loaded from the file.")
        except Exception as e:
            raise ValueError(f"Error loading document: {str(e)}")

        # Get chunk settings and create text splitter
        chunk_settings = self._get_chunk_settings(file_path)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_settings['chunk_size'],
            chunk_overlap=chunk_settings['chunk_overlap'],
            separators=["\n\n", "\n", " ", ""]
        )

        # Split documents
        try:
            splits = text_splitter.split_documents(docs)
            if not splits:
                raise ValueError("No text chunks were created from the documents.")
        except Exception as e:
            raise ValueError(f"Error splitting document: {str(e)}")

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
            raise ConnectionError(f"Failed to connect to Qdrant: {str(e)}")

        return "✅ Vector DB Successfully Created and Stored in Qdrant!"
