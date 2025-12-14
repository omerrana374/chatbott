import os
import json
import re

DOCS_FOLDER = "docs"

# def load_all_docs():
#     """
#     Loads all text-based documentation files from teacher_bot/docs/
#     Supports .txt, .md, .json, .jsonl
#     Returns list of dicts: { "text": "...", "source": filename }
#     """
#     base_path = os.path.join(os.path.dirname(__file__), DOCS_FOLDER)

#     if not os.path.exists(base_path):
#         return []

#     docs = []

#     for fname in os.listdir(base_path):
#         path = os.path.join(base_path, fname)

#         if fname.endswith(".txt") or fname.endswith(".md"):
#             with open(path, "r", encoding="utf8") as f:
#                 docs.append({"text": f.read(), "source": fname})

#         elif fname.endswith(".json"):
#             with open(path, "r", encoding="utf8") as f:
#                 data = json.load(f)
#                 docs.append({"text": json.dumps(data, indent=2), "source": fname})

#         elif fname.endswith(".jsonl"):
#             with open(path, "r", encoding="utf8") as f:
#                 for line in f:
#                     try:
#                         obj = json.loads(line)
#                         docs.append(
#                             {"text": json.dumps(obj, indent=2), "source": fname}
#                         )
#                     except:
#                         pass

#     return docs


def parse_feature_overview(text: str):
    """
    Parses FAQ-style document into Q/A chunks.
    Each question + answer becomes one embedding unit.
    """
    chunks = []

    parts = re.split(r"\nQ\d+\.\s*", text)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        lines = part.split("\n", 1)
        question = lines[0].strip()
        answer = lines[1].strip() if len(lines) > 1 else ""

        chunk_text = f"Question: {question}\nAnswer: {answer}"
        chunks.append(chunk_text)

    return chunks


def parse_codebase_explanation(text: str):
    """
    Parses heading-based technical documentation.
    Each numbered heading + its content becomes one chunk.
    """
    chunks = []

    sections = re.split(r"\n(?=\d+\)\s)", text)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split("\n", 1)
        heading = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""

        chunk_text = f"Section: {heading}\n{content}"
        chunks.append(chunk_text)

    return chunks


def load_all_docs():
    """
    Loads and normalizes documentation files from teacher_bot/docs/

    Returns:
        List of dicts: { "text": "...", "source": filename }
    """
    base_path = os.path.join(os.path.dirname(__file__), DOCS_FOLDER)

    if not os.path.exists(base_path):
        return []

    docs = []

    for fname in os.listdir(base_path):
        path = os.path.join(base_path, fname)

        if fname.endswith(".txt") or fname.endswith(".md"):
            with open(path, "r", encoding="utf8") as f:
                text = f.read()

            if fname == "feature_overview.txt":
                chunks = parse_feature_overview(text)

            elif fname == "codebase_explanation.txt":
                chunks = parse_codebase_explanation(text)

            else:
                chunks = [text]

            for chunk in chunks:
                docs.append(
                    {
                        "text": chunk,
                        "source": fname,
                    }
                )

        elif fname.endswith(".json"):
            with open(path, "r", encoding="utf8") as f:
                data = json.load(f)
                docs.append(
                    {
                        "text": json.dumps(data, indent=2),
                        "source": fname,
                    }
                )

        elif fname.endswith(".jsonl"):
            with open(path, "r", encoding="utf8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        docs.append(
                            {
                                "text": json.dumps(obj, indent=2),
                                "source": fname,
                            }
                        )
                    except:
                        pass

    return docs
