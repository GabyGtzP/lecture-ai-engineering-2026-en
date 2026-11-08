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
- What you did: I installed Pi, selected Gemini 3.5 Flash Lite, and reviewed Pi's [public system-prompt implementation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/system-prompt.ts). For a bounded, safe test that would not inspect or modify this repository, I ran Pi in print mode with its tools disabled and asked it to describe its role.
- Results: Pi described itself as a coding assistant that can inspect codebases, modify code, run commands and tests, and customize the Pi harness. Its source constructs a modular prompt rather than relying on one role paragraph: a role preamble, enabled-tool descriptions, tool and user-configured rules, documentation guidance, and (when available) project context, skills, and the current working directory. With default settings, the source selects read, bash, edit, and write tools. The exact prompt can therefore vary with configuration and workspace context.
- Observations and questions:

  | Dimension | Pi coding agent | AIE2026 learning support agent |
  |---|---|---|
  | Primary role | General coding assistant: inspect a repository, execute development tasks, and modify files. | Course-specific learning assistant for AIE2026. |
  | Tool guidance | Describes the enabled coding tools and adds operational rules based on the selected tools and configuration. Default tools include file reading, shell commands, editing, and writing. | instructions name the intended tools for particular tasks: search the glossary for course terms, and use lecture summaries for session-content questions. The tools' docstrings in `app/tools.py` further describe their arguments and use. |
  | Source of grounding | Can incorporate workspace/project context and local skills when present; its prompt also includes guidance for consulting Pi documentation on harness-related questions. | Uses the course glossary and lecture summaries as explicit sources. It instructs the model to say when information is absent from the glossary rather than guess. |
  | Desired interaction | Helps users accomplish software-development tasks; the prompt also asks for concise responses and clear file paths. | Supports learning: identify the relevant lecture and offer hints instead of simply doing homework for the learner. |
  | Scope and flexibility | Broad and configurable. Its assembled instructions can change with enabled tools, settings, project context, skills, and custom prompt additions. | Narrower and domain-specific. The role and guidance are stable in instructions, while capabilities are supplied through the registered tools and their descriptions. |

  The central design difference is not merely that the agents have different roles: their prompts reflect different evidence and action models. Pi is designed to operate on a changing software workspace, so its prompt couples tool affordances with operational guidance and available project context. The AIE2026 agent is designed to answer within a defined course domain, so its instructions emphasize retrieving authoritative course material and communicating uncertainty when that material is missing. In both systems, instructions and tools work together: a prompt can encourage a tool call, but the tool descriptions and actual registration determine what the model can call and what information it receives.

  This comparison is based on the published Pi prompt-construction code and our local instructions and tool docstrings. The Pi runtime test was deliberately limited to one response with tools disabled; it confirmed the general role description but did not experimentally verify file operations, tool-selection behavior, or answer quality on the Lecture 03 questions. A direct behavioral comparison would require running the same questions on both agents with comparable models, tool access, and context, then comparing their outputs and tool traces. Pi's assembled prompt is configuration- and workspace-dependent, so the public implementation describes how it is built rather than one universal prompt string.

  Questions raised by these observations:
  - If both agents receive the same model, question, and relevant context, how do their answers and tool calls differ?
  - Does explicitly requiring glossary lookup reduce unsupported claims compared with an agent that can use workspace context but has no course-specific grounding instruction?
  - How do Pi's dynamically assembled prompt sections (enabled tools, project context, and skills) affect its behavior when those sections are changed or removed?
  - How should an evaluation balance coding-task success against learning goals such as giving hints, citing course material, and acknowledging uncertainty?
