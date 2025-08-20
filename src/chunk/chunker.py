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

import ast, re, pandas as pd
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
            parts.append(f"{col.capitalize()}: {formatted_stat}" )
            """
            if col == "attack" or col == "defence":
                summary = summarize_stats(formatted_stat, col, category)
                parts.append(f"{col.capitalize()} Summary: {summary}" )
            """
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
            return ", ".join([item.strip("\"'") for item in parsed])
        # If its a regular dict (stats)
        if isinstance(parsed, dict):
            return ", ".join([f"{key}: {value}" for key, value in parsed.items()])

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

    return ", ".join(formatted)

def clean_chunk(raw_chunk: str) -> str:
    """
    Cleans raw weapon chunk text into a natural language format for better embeddings.
    """
    lines = raw_chunk.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        label, stats = line.split(":", 1)
        stats = stats.strip()
        if not stats:
            continue
        if line.startswith("Attack:") or line.startswith("Defence:"):
            label = label.strip()
            stat_parts = [
                f"{expand_stat_label(stat.strip().split(":")[0])}{stat.strip().split(":")[1]}"
                for stat in stats.split(",") if ":" in stat
            ]
            cleaned_lines.append(f"{label} Stats: {', '.join(stat_parts)}")

        elif line.startswith("Scales_with:"):
            parts = []
            for stat in stats.split(","):
                key, val = stat.strip().split(":")
                parts.append(f"{expand_attr_label(key.strip())} at grade {val.strip()}")
            cleaned_lines.append(f"This weapon scales with {', '.join(parts)}.")

        elif line.startswith("Required_attributes:"):
            parts = []
            for stat in stats.split(","):
                key, val = stat.strip().split(":")
                parts.append(f"{expand_attr_label(key.strip())} {val.strip()}")
            cleaned_lines.append(f"Requirements: {', '.join(parts)}.")

        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

"""
def summarize_stats(stats, col, category):
    stats_dict = dict()
    stat_list = stats.split(',')
    category = category[0:len(category)-1]


    for stat in stat_list:
        name_val = stat.split(':')
        label = expand_stat_label(name_val[0].strip())
        val = name_val[1].strip()
        val = 0 if not val.isdigit() else int(val)
        stats_dict[label] = val

    summary = []
    dmg_def = "damage" if col == "attack" else "defence"

    if stats_dict.get("Physical", 0) > 130:
        summary.append(f"high physical {dmg_def}")
    if stats_dict.get("Critical", 0) >= 100:
        summary.append("excellent critical strike potential")
    if stats_dict.get("Guard Boost", 0) >= 30:
        summary.append("excellent Guard Boost")
    if all(stats_dict.get(stat, 0) == 0 for stat in ["Magic", "Fire", "Lightning", "Holy"]):
        summary.append(f"no elemental {dmg_def}")
    for stat in ["Magic", "Fire", "Lightning", "Holy"]:
        if stats_dict.get(stat, 0) > 50:
            summary.append(f"high {stat} {dmg_def}")

    return f"This {category} has " + ', '.join(summary)
"""
def expand_stat_label(label):
    return {
        "Phy": "Physical",
        "Mag": "Magic",
        "Fire": "Fire",
        "Ligt": "Lightning",
        "Holy": "Holy",
        "Crit": "Critical",
        "Boost": "Guard Boost"
    }.get(label, label)

def expand_attr_label(label):
    return {
        "Str": "Strength",
        "Dex": "Dexterity",
        "Fai": "Faith",
        "Int": "Intelligence",
        "Arc": "Arcane"
    }.get(label, label)









