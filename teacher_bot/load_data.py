import json
import os
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

BASE_DIR = CURRENT_DIR.parent

RAW_DATA_PATH = BASE_DIR / "instruction_format_dataset.jsonl"
SYNTHETIC_PATH = BASE_DIR / "synthetic.jsonl"


def load_jsonl(path):
    print("Loading from:", path)
    with open(path, "r") as f:
        for line in f:
            yield line


def load_jsonl(path):
    """Load a JSONL file and return a list of dicts."""
    records = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def extract_records(data):
    """Extract indexable text + answer."""
    cleaned = []

    for row in data:
        inp = row.get("input", {})
        out = row.get("output", {})

        component = inp.get("Component Tag", "")
        problem = inp.get("Problem Description", "")
        tag = inp.get("Problem Tag", "")
        solution = out.get("Solution", "")

        searchable_text = f"{component}. {tag}. {problem}".strip()

        cleaned.append({"text": searchable_text, "solution": solution})

    return cleaned


def load_all_data():
    real = load_jsonl(RAW_DATA_PATH)
    synthetic = load_jsonl(SYNTHETIC_PATH)

    real_clean = extract_records(real)
    synthetic_clean = extract_records(synthetic)

    combined = real_clean + synthetic_clean
    return combined
