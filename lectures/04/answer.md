# Lecture 04 Answers

## Exercises

I labeled all ten cases in Streamlit and compared them with the instructor labels. All five judgment fields matched on all 10 cases. I marked #07 (whether an out-of-scope refusal needs a lecture marker) as unsure.

I ran the real grader with `gemini-3.5-flash-lite`.

- Agreement before rubric revision: Grounding 9/10, Scope 10/10, Hint 10/10, Clarity 9/10, Lecture marker 10/10. Overall agreement was 10/10 with 100% automatic coverage; no items were marked for review.
- Disagreements before revision: #04 Clarity (LLM pass, human fail) and #08 Grounding (LLM fail, human pass).
- Criterion revised: Grounding. I clarified that Grounding is about factual support or contradiction; expected-behavior and role compliance should be judged under the appropriate criterion, such as Scope. I added this policy to `data/eval/rubric.md`.
- Agreement after revision: Grounding 9/10, Scope 10/10, Hint 10/10, Clarity 9/10, Lecture marker 10/10. Overall agreement remained 10/10 with 100% automatic coverage; no items were marked for review.
- Disagreements after revision: #04 Clarity (LLM pass, human fail) and #06 Grounding (LLM fail, human pass).

The revision did not change the agreement totals or review count, and the Grounding disagreement moved from #08 to #06. The LLM treated expected behavior as a Grounding issue in #06 even though the answer's complete homework code is more directly a Hint failure. This illustrates why criteria should be judged independently and why disagreements need human review. The lecture marker is suited to a deterministic code check; grounding, scope, hint quality, and especially clarity need rubric-based judgment and human oversight.

## Homework

- Level attempted: Advanced
- Benchmark: [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified), a verified 500-task subset of real GitHub software issues. The dataset viewer shows the issue statement, repository/version, reference patch, test patch, and tests for each task.
- Problems read in the [Hugging Face Dataset Viewer](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/viewer/default/test):
  - `astropy__astropy-12907`: A nested compound astronomy model gives an incorrect separability matrix. I think I could investigate this by reproducing the matrix and following how nested models are combined. An LLM would need to trace the interaction between nested structures and matrix calculations, rather than only recognize the API.
  - `astropy__astropy-13033`: Removing a required time-series column produces a misleading validation error when multiple columns are required. I think I could work from the reproduction and expected error behavior. An LLM would need to find where the validation assumes only one required column and preserve the behavior for the existing cases.
  - `astropy__astropy-13236`: Structured NumPy arrays are automatically converted to a mixin, and the issue proposes removing that conversion. I think I could explore it with the tests, including masked structured arrays. An LLM would need to understand the table's existing array behavior and avoid regressions across the different array forms.

  These are repository-level maintenance tasks, not self-contained coding puzzles. The first viewer entry estimates 15 minutes to 1 hour. All three require understanding project context and validating a change with tests; for an LLM, locating the relevant code and making a patch that fixes the reported behavior without breaking other behavior are likely harder than generating a short code snippet.

- Contributors and validation: OpenAI's [SWE-bench Verified announcement](https://openai.com/index/introducing-swe-bench-verified/) reports that 93 software engineers reviewed 1,699 candidate tasks, with three independent reviewers per task. 500 tasks were included in Verified; 1,199 of the reviewed candidates were not included. The review assessed whether issues were well specified and solvable and whether their tests were appropriate.
- Grading: A model receives an issue and repository snapshot and produces a patch. The evaluation harness applies the patch and runs issue-specific fail-to-pass tests plus regression pass-to-pass tests; a task is resolved when the patch applies and all required tests pass. This is executable test-based grading, rather than an LLM judging a prose answer. See the [SWE-bench paper](https://arxiv.org/abs/2310.06770) and [official project documentation](https://www.swebench.com/SWE-bench/).
- Comparison with Lecture 04: Today's evaluation set has ten prepared question/answer cases. A human labels them and an LLM judges Grounding, Scope, Hint, and Clarity, while code checks the lecture marker. SWE-bench Verified has 500 repository issues paired with code and tests; proposed code patches are scored by test outcomes. Both require careful case curation, but Verified uses multiple independent reviewers and mostly automated, executable checks, while Lecture 04 focuses on rubric-based judgments, human/LLM agreement, and identifying cases that need human review.
