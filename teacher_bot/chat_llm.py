import subprocess
import json


def call_llm(prompt: str) -> str:
    cmd = ["ollama", "run", "phi3.5:latest"]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    out, err = process.communicate(input=prompt)

    if err:
        print("Error:", err)
    print("out === ", out)
    return out.strip()
