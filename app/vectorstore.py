from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.embeddings import get_embedding_model


DB_PATH = "./chroma_db"
DATA_PATH = Path("./data")


def create_vector_store():

    documents = []

    # Load every TXT file from the data directory
    for file_path in DATA_PATH.glob("*.txt"):

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        file_documents = loader.load()

        documents.extend(file_documents)

        print(
            f"Loaded {file_path.name}: "
            f"{len(file_documents)} document(s)"
        )

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    # Embedding model
    embedding_model = get_embedding_model()

    # Create ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    return vector_store


def load_vector_store():

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )

    return vector_store