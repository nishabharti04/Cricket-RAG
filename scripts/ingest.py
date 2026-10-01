from app.vectorstore import create_vector_store


if __name__ == "__main__":

    print("Starting document ingestion...")

    create_vector_store()

    print("Documents successfully stored in ChromaDB.")