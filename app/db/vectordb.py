import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from git import Repo
from app.config import (EMBEDDING_MODEL, QDRANT_URL,
                        QDRANT_TOKEN, QDRANT_COLLECTION_NAME)


class RAG:
    """
    RAG (Repository Analysis and Generation) class.

    This class represents a repository analysis and generation system.
    It provides methods to clone repositories from GitHub, load source code documents,
    split documents into smaller chunks, and store vectors in the Qdrant index.

    Attributes:
        repos (List[str]): A list of repository paths.

    Methods:
        __init__(): Initializes the RAG class.
        __repo_clone(): Clone multiple repositories from GitHub.
        __source_code_loader(source_code_path): Load source code documents from the given path.
        __doc_splitter(documents): Split documents into smaller chunks.
        vector_store(): Store vectors in the Qdrant index.
    """

    def __init__(self):
        self.repos = [
            "tiangolo/fastapi",
            "bslatkin/effectivepython",
            "kacos2000/Queries"
        ]
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_TOKEN
        )

    def __repo_clone(self):
        """
        Clone multiple repositories from GitHub.

        This method clones multiple repositories from GitHub using the `gitpython` library.
        It takes no arguments and doesn't return anything.

        Example usage:
            db = VectorDB()
            db.repo_clone()
        """
        for repo_path in self.repos:
            if os.path.isdir(repo_path):
                repo = Repo(repo_path) 
                repo.remotes.origin.pull()
            else:
                Repo.clone_from(
                    f"https://github.com/{repo}",
                    to_path=f"github-repos/{repo}"
                )
    
    def __source_code_loader(self, source_code_path):
        """
        Load source code documents from the given path.

        Args:
            source_code_path (str): The path to the source code directory.

        Returns:
            List[Document]: A list of loaded documents.
        """
        self.__repo_clone()
        loader = GenericLoader.from_filesystem(
            source_code_path,
            glob="**/*",
            suffixes=[".py", ".sql"],
            parser=LanguageParser(
                language=Language.PYTHON,
                parser_threshold=1000
            )
        )
        documents = loader.load()
        return documents
    
    def __doc_splitter(self, documents):
        """
        Split documents into smaller chunks.

        Args:
            documents (List[Document]): A list of documents to split.

        Returns:
            List[Document]: A list of split documents.
        """
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=256,
            chunk_overlap=0,
            length_function=len,
        )

        return python_splitter.split_documents(documents)
    
    def hf_embedding(self):
        """
        Returns the HuggingFaceEmbeddings object for the specified model.

        Returns:
            HuggingFaceEmbeddings: The HuggingFaceEmbeddings object.
        """
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                'device': 'cpu'
            },
            encode_kwargs={
                "normalize_embeddings": False
            }
        )

        return embeddings

    def vector_store(self):
        """
        Store vectors in the Qdrant index.

        Returns:
            qdrant_rsp: Response from Qdrant indicating the success of the operation.
        """
        sql_code = self.__source_code_loader("github-repos/kacos2000/Queries")
        python_code = self.__source_code_loader("github-repos/bslatkin/effectivepython/example_code")
        fastapi_code = self.__source_code_loader("github-repos/tiangolo/fastapi/fastapi")
        source_codes = sql_code + python_code + fastapi_code

        documents = self.__doc_splitter(source_codes)
        qdrant_rsp = Qdrant.from_documents(
            documents,
            self.hf_embedding(),
            url=QDRANT_URL,
            api_key=QDRANT_TOKEN,
            prefer_grpc=True,
            collection_name=QDRANT_COLLECTION_NAME,
        )

        return qdrant_rsp
    
    def vector_retriever(self, k=3):
        """
        Perform a vector search using the QdrantClient.

        Args:
            k (int): The number of results to return.

        Returns:
            doc_retriever: A Qdrant retriever object for similarity search.
        """
        doc_store = Qdrant(
            client=self.qdrant_client,
            collection_name=QDRANT_COLLECTION_NAME,
            embeddings=self.hf_embedding()
        )

        # similarity search works best for this case
        doc_retriever = doc_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k
            }
        )

        return doc_retriever
