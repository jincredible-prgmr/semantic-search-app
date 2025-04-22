"""
chunker.py

Handles logic to convert row to chunks
- Data formatting to make it easily chunkable/readable 
- Deciding which fields to chunk given the category

Functions:
- row_to_chunk(): Compiles and returns field values
- safe_parse_stat_field(): Safely parses "special" fields that require extra formatting -> returns parsed field value
- format_stats(stat_list): Formats list of dicts to readable chunk
"""

import pandas as pd
import ast
from config import field_config, special_fields


def row_to_chunk(row, category):
    """
    Based on category type, iterates through desired fields (cols) converts values to string, and compiles/returns values

    Args:
        row (pandas row): current row to be chunked
        category (str): Data category (e.g. 'Spell', 'Item', 'NPC').

    Returns:
        Str: Chunked row data
    """
    fields = field_config.get(category, [])
    special = special_fields.get(category, {})

    parts = []

    for col in fields:
        if col in special:
            formatted_stat = safe_parse_stat_field(row[col])
            parts.append(f"{col.capitalize()}:\n{formatted_stat}" )
        else:
            parts.append(f"{col.capitalize()}: {row[col]}" )

    return f"Category: {category}\n" + "\n".join(parts)


def safe_parse_stat_field(field):
    """
    Safely parses "special" fields that require extra formatting

    Args:
        field (pandas val): field data to be parsed

    Returns:
        Str: Parsed field data
    """
    if pd.isnull(field):
        return ''
    
    try:
        # Try to parse the string
        parsed = ast.literal_eval(field)

        # If it's a list of dicts (attack/defense/scaling etc)
        if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
            return format_stats(parsed)
        # If it's a list of strs -> strip additional " creating issues (drops)
        if isinstance(parsed, list):
            return "\n".join([item.strip("\"'") for item in parsed])
        # If its a regular dict (stats)
        if isinstance(parsed, dict):
            return "\n".join([f"{key}: {value}" for key, value in parsed.items()])

        # Fallback to string
        return str(parsed)

    except (ValueError, SyntaxError):
        print(f"Warning: Could not parse field: {field}")
        return str(field)  # Safe fallback
    

def format_stats(stat_list):
    """
    Formats list of dicts to readable chunk str

    Args:
        stat_list (List[Dict]): field data to be parsed

    Returns:
        Str: Parsed field data
    """
    formatted = []

    for entry in stat_list:
        if 'amount' in entry:
            formatted.append(f"{entry['name']}: {entry['amount']}")
        elif 'scaling' in entry:
            formatted.append(f"{entry['name']}: {entry['scaling']}")
        else:
            formatted.append(str(entry))  # fallback if weird dict

    return "\n".join(formatted)








