"""
app.py

Streamlit semantic search UI for Elden Ring data.

Usage:
    streamlit run app.py
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from embedding import get_embedding_function
from vector_store import query, collection_count
from config import categories


@st.cache_resource
def load_embedding_fn():
    return get_embedding_function()


st.set_page_config(page_title="Elden Ring Search", page_icon="⚔️", layout="wide")
st.title("Elden Ring Semantic Search")

count = collection_count()
if count == 0:
    st.error("No data found. Run `python ingest.py` first to embed and store the data.")
    st.stop()

st.caption(f"{count} items indexed")

col1, col2, col3 = st.columns([4, 2, 1])
with col1:
    search_query = st.text_input(
        "Search",
        placeholder="e.g. 'a sword that scales with intelligence'",
        label_visibility="collapsed",
    )
with col2:
    selected_category = st.selectbox("Category", ["All"] + categories)
with col3:
    n_results = st.number_input("Results", min_value=1, max_value=20, value=5)

if search_query:
    embedding_fn = load_embedding_fn()
    category_filter = selected_category if selected_category != "All" else None

    with st.spinner("Searching..."):
        results = query(search_query, embedding_fn, n_results=n_results, category=category_filter)

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    if not docs:
        st.info("No results found.")
    else:
        st.subheader(f"Top {len(docs)} results")
        for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
            similarity = round((1 - dist) * 100, 1)
            category_label = meta.get("category", "Unknown")
            # Extract the name from the chunk text (second line: "Name: ...")
            name_line = next((l for l in doc.splitlines() if l.startswith("Name:")), None)
            title = name_line.replace("Name:", "").strip() if name_line else f"Result {i + 1}"

            with st.expander(f"**{title}** — {category_label} &nbsp; `{similarity}% match`", expanded=i == 0):
                st.text(doc)
