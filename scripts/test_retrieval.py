from app.rag import CricketRAG


rag = CricketRAG()

question = "Who won the 1983 Cricket World Cup?"

print("=" * 70)
print("QUESTION:")
print(question)

results = rag.vector_store.similarity_search_with_score(
    question,
    k=3
)

print("\nRETRIEVED DOCUMENTS:")

for i, (doc, score) in enumerate(results, start=1):

    print(f"\n--- Document {i} ---")
    print(f"Distance Score: {score}")
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
    print("\nContent:")
    print(doc.page_content)