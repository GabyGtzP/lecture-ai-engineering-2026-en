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

- Level attempted: Advanced (option B)
- What you did: I installed Pi, selected Gemini 3.5 Flash Lite, reviewed Pi's [public system-prompt implementation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/system-prompt.ts), and ran Pi with its standard tool set in a temporary copy of `app/agent.py` and `app/tools.py`. I asked Pi to compare its role and tool-use guidance with the AIE2026 instructions and did not ask it to modify files.
- Results: Pi returned a comparison that characterized itself as a general coding assistant and the AIE2026 agent as a course-specific tutor. It identified the course agent's glossary lookup, lecture-summary, quiz, uncertainty, and hint-giving rules, and contrasted these with Pi's file and shell tools. The source confirms that Pi assembles its prompt from a role preamble, enabled-tool descriptions, rules, documentation guidance, and optional project context, skills, and working-directory information. Its default tools include `read`, `bash`, `edit`, and `write`; the actual prompt and capabilities can vary with configuration and workspace.
- Observations and questions:

  | Dimension | Pi coding agent | AIE2026 learning support agent |
  |---|---|---|
  | Primary role | General coding assistant: inspect a repository, execute development tasks, and modify files. | Course-specific learning assistant for AIE2026. |
  | Tool guidance | Describes enabled coding tools and adds operational rules based on the selected tools and configuration. The Pi run had the standard `read`, `bash`, `edit`, and `write` tools available. | `INSTRUCTIONS` name intended tools for particular tasks: search the glossary for course terms, use lecture summaries for session-content questions, and create review questions with `make_quiz`. Docstrings in `app/tools.py` describe their arguments and use. |
  | Source of grounding | Can incorporate workspace/project context and local skills when present; its prompt also includes guidance for consulting Pi documentation on harness-related questions. | Uses the course glossary and lecture summaries as explicit sources. It instructs the model to say when information is absent from the glossary rather than guess. |
  | Desired interaction | Helps users accomplish software-development tasks; the prompt also asks for concise responses and clear file paths. | Supports learning: identify the relevant lecture and offer hints instead of simply doing homework for the learner. |
  | Scope and flexibility | Broad and configurable. Its assembled instructions can change with enabled tools, settings, project context, skills, and custom prompt additions. | Narrower and domain-specific. The role and guidance are stable in instructions, while capabilities are supplied through the registered tools and their descriptions. |

  The central design difference is not merely that the agents have different roles: their prompts reflect different evidence and action models. Pi is designed to operate on a changing software workspace, so its prompt couples tool affordances with operational guidance and available project context. The AIE2026 agent is designed to answer within a defined course domain, so its instructions emphasize retrieving authoritative course material and communicating uncertainty when that material is missing. In both systems, instructions and tools work together: a prompt can encourage a tool call, but the tool descriptions and actual registration determine what the model can call and what information it receives.

  This comparison combines the published Pi prompt-construction code, the local instructions and tool docstrings, and Pi's runtime response after inspecting a temporary copy of the two app files. The agents were not given the same Lecture 03 question in a controlled experiment, so this work compares their roles and prompt/tool designs rather than relative answer quality. Pi's assembled prompt is configuration- and workspace-dependent; the public implementation describes how it is built rather than one universal prompt string.

  Questions raised by these observations:
  - If both agents receive the same model, question, and relevant context, how do their answers and tool calls differ?
  - Does explicitly requiring glossary lookup reduce unsupported claims compared with an agent that can use workspace context but has no course-specific grounding instruction?
  - How do Pi's dynamically assembled prompt sections (enabled tools, project context, and skills) affect its behavior when those sections are changed or removed?
  - How should an evaluation balance coding-task success against learning goals such as giving hints, citing course material, and acknowledging uncertainty?
