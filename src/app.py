from load_data import load_category_data
from embedding import embed_store_chunks, get_embedding_fn
from langchain.vectorstores import Chroma



def test_embed_subset(category):
    chunks = load_category_data(category)
    chunks_subset = [chunks[x] for x in range(10)]
    embed_store_chunks(chunks_subset)


embedding_fn = get_embedding_fn()
vector_store = Chroma(
    persist_directory="chroma_db/",  # must match what you used when saving
    embedding_function=embedding_fn
)
query = "What sword has the highest physical attack?"
results = vector_store.similarity_search(query, k=3)
for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)









