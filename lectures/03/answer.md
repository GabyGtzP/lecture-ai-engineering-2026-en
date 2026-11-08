# Lecture 03 Answers

## Exercises

| | Lecture 01 `app.ask` (bare LLM) | Lecture 03 agent (terminal) |
|---|---|---|
| Answer | The exact response was not recorded in `lectures/01/answer.md`, so a word-for-word comparison is not possible. | “In the AIE2026 course, homework is structured into **3 homework levels** designed to suit different learning paces and goals:<br><br>1. **Basic**: Focuses on reviewing the lecture content.<br>2. **Implementation**: Involves writing your own code.<br>3. **Advanced**: Involves research and experimentation.<br><br>As a general rule, completing **any one** of these levels is enough to complete the homework for that lecture, and they are not graded.<br><br>If you are deciding which level to tackle, try starting with *Basic* to solidify your understanding of the core concepts, or push yourself to *Implementation* and *Advanced* if you want hands-on coding practice and deeper experimentation!” |
| Comparison with the glossary | Cannot verify without the original response. | Correctly gives all three levels and says any one level is sufficient and homework is not graded, matching the `homework-levels` entry in `data/glossary.json`. |

The agent was able to look up this course-specific information in the glossary. To complete a direct comparison, add the response you got from `app.ask` in Lecture 01.
- Tool calls shown by `--trace` (tool names and arguments): `search_glossary({'query': 'LoRA'})`. It returned the glossary definition for LoRA, which the agent used to answer and identify Lecture 02.
- Number of LLM calls for one question (`requests`): 2 (one tool call).
- Tool added and the description in its docstring: `make_quiz(lecture: int)` creates a review question and answer from a glossary term for the requested lecture. Its docstring tells the agent to use it when a learner asks for a quiz or review question.
- `make_quiz` trace check: The prompt “Give me one review question from Lecture 02” called `make_quiz({'lecture': 2})`. It returned a question about LoRA; the agent presented it with a hint and identified Lecture 02. This run used 2 requests and 1 tool call.

## Homework

- Level attempted: Basic / Implementation / Advanced
- What you did:
- Results:
- Observations and questions:
