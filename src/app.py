from load_data import load_data
from embedding import embed_chunks, query_db, get_vector_store
from retriever import get_rag


"""
chunks = load_data()
embed_chunks(chunks)
"""



#query_db("Sword with attack stat 98", 6)
"""
qa = get_qa()
res = qa.run('What is the best sword?')

print(res)
"""

"""retriever = get_retriever()
docs = retriever.get_relevant_documents("What is the best weapon and why?")
print(len(docs))
for d in docs:
    print(d.metadata, d.page_content[:150])
"""

rag = get_rag(k=5, search_type="mmr")
out = rag.invoke({"input": "Which sword has the greatest magic attack?"})
print(out["answer"])
# If you want to see the retrieved docs:
for i, d in enumerate(out["context"], 1):
    print(f"\n--- DOC {i} ---\n{d.metadata}\n{d.page_content[:500]}")










