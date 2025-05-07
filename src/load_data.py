"""
load_data.py

Handles loading and chunking of all Elden Ring dataset categories.

Functions:
- load_data(): Master loader combining all categories.
- load_category(): Generic loader for any category.
- test_cat(): Testing function used to get single category's chunks
"""
import pandas as pd
import os
from config import categories, DATA_DIR
from chunker import row_to_chunk, clean_chunk


def load_data() -> list:
    """
    Loads and compiles all category chunks into a flattened list of chunks (dict objects)

    Args:
        N/A

    Returns:
        List[Dict]: Chunked data ready for embedding [{"id":"000", "chunk" : "chunk data", "metadata" : {"Category" : "xxx"}}, ...].
    """
    return [chunk for category in categories for chunk in load_category_data(category)]



def load_category_data(category) -> list:
    """
    Loads a specific CSV and returns cleaned chunked data.

    Args:
        category (str): Data category (e.g. 'Spell', 'Item', 'NPC').

    Returns:
        List[Dict]: Chunked data ready for embedding.
    """
    path = os.path.join(DATA_DIR, f"{category.lower()}.csv")
    df = pd.read_csv(path, index_col=False)

    # Build chunk dict with cleaned content and metadata
    return [
        {
            "id" : row['id'],
            "chunk" : clean_chunk(row_to_chunk(row, category)),
            "metadata" : {"category" : category}
        }
        for idx, row in df.iterrows()
    ]


def test_cat(category):
    print(load_category_data(category)[0].get('chunk'))

def get_one_chunk(category):
    return load_category_data(category)[0]

#test_cat('Weapons')
load_data()

    








