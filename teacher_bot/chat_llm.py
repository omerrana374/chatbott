# import subprocess
# import json


# def call_llm(prompt: str) -> str:
#     cmd = ["ollama", "run", "phi3.5:latest"]

#     process = subprocess.Popen(
#         cmd,
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#     )

#     out, err = process.communicate(input=prompt)

#     if err:
#         print("Error:", err)
#     print("out === ", out)
#     return out.strip()


import requests

OLLAMA_URL = "http://ollama:11434/api/generate"


def call_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()
