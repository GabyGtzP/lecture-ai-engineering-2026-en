"""Tests for the Lecture 01 ask script without calling the Gemini API."""

from types import SimpleNamespace

from app import ask as ask_module


def test_ask_displays_response_time_and_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="answer",
        usage_metadata=SimpleNamespace(prompt_token_count=3, candidates_token_count=5),
    )
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: response)
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)
    times = iter([1.0, 2.5])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(times))

    assert ask_module.ask("question") == "answer"
    output = capsys.readouterr().out
    assert "[timing] response=1.50s" in output
    assert "[tokens] input=3 output=5" in output


def test_interactive_mode_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, question):
            self.questions.append(question)
            return SimpleNamespace(
                text=f"answer to {question}",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=1, candidates_token_count=2
                ),
            )

    chat = FakeChat()
    client = SimpleNamespace(chats=SimpleNamespace(create=lambda **kwargs: chat))
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)
    questions = iter(["first question", "follow-up", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(questions))
    times = iter([1.0, 1.1, 2.0, 2.2])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(times))

    ask_module.run_interactive()

    assert chat.questions == ["first question", "follow-up"]
    output = capsys.readouterr().out
    assert "answer to first question" in output
    assert "answer to follow-up" in output