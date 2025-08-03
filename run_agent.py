import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-4")

def load_prompt(role: str) -> str:
    path = Path(f"roles/{role}.txt")
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, "r") as f:
        return f.read()

def log_output(role: str, output: str):
    log_path = Path(f"workspace/agent_logs/{role}.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(output + "\n---\n")

def call_llm(prompt: str) -> str:
    if LLM_PROVIDER.startswith("openai"):
        return call_openai(prompt)
    elif LLM_PROVIDER.startswith("claude"):
        return call_claude(prompt)
    else:
        raise ValueError("Unknown LLM provider")

def call_openai(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL.replace("openai/", ""),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def call_claude(prompt: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": MODEL.replace("claude/", ""),
        "max_tokens": 1024,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["content"][0]["text"].strip()

def main(role: str):
    print(f"[{role}] Agent starting...\n")
    prompt = load_prompt(role)
    print("=== Initial Role Prompt ===")
    print(prompt)
    print("===========================\n")

    while True:
        try:
            user_input = input(">>> ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("Exiting agent.")
                break

            full_prompt = f"{prompt}\n\nUser input:\n{user_input}"
            response = call_llm(full_prompt)
            print("\n💬 LLM Response:\n", response)
            log_output(role, f"USER: {user_input}\nLLM: {response}")
        except KeyboardInterrupt:
            print("\n[Interrupt] Exiting agent.")
            break
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, help="Role name (matches roles/*.txt)")
    args = parser.parse_args()
    main(args.role)

