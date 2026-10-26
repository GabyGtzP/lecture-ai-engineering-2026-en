"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied
    uv run python -m app.ask --interactive  # Keep history for follow-up questions

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask(question: str, chat=None) -> str:
    client = genai.Client(api_key=get_api_key()) if chat is None else None
    started_at = time.perf_counter()
    if chat is None:
        response = client.models.generate_content(model=MODEL, contents=question)
    else:
        response = chat.send_message(question)
    elapsed = time.perf_counter() - started_at

    print(f"[timing] response={elapsed:.2f}s")
    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[tokens] input={usage.prompt_token_count} "
            f"output={usage.candidates_token_count}"
        )

    return response.text


def run_interactive() -> None:
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)
    print("[interactive] Enter 'exit' or 'quit' to finish.")
    while True:
        try:
            question = input("\n[you] ").strip()
        except EOFError:
            break
        if question.lower() in {"exit", "quit"}:
            break
        if question:
            print(ask(question, chat=chat))


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--interactive", action="store_true", help="Keep conversation history for follow-up questions")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.interactive:
            run_interactive()
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[question] {question}\n")
            print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
