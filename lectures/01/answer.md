# Lecture 01 Answers

## Exercises

Model used: `gemini-3.5-flash-lite`.

- Model's answer: It described Foundation/Basic, Intermediate/Application, and Advanced/Mastery as typical course levels.
- Comparison with the glossary: The answer sounded plausible but was not course-specific. The glossary defines Basic as reviewing lecture content, Implementation as writing code, and Advanced as research and experimentation.
- Token counts for the course-specific question: 18 input / 295 output.
- Measured response time: 3.72 seconds.

## Homework

### Basic

Ran the same question three times: "In no more than 2 sentences, what is LoRA?" The temperature was left at its default; I changed the model for the third run.

| Run | Model | Response time | Input / output tokens |
|---|---|---:|---:|
| 1 | `gemini-3.5-flash-lite` | 0.63 s | 14 / 55 |
| 2 | `gemini-3.5-flash-lite` | 0.66 s | 14 / 55 |
| 3 | `gemini-3.8-flash` | 38.29 s | 14 / 64 |

All three correctly described LoRA as parameter-efficient fine-tuning that keeps the base weights frozen and trains a smaller set of parameters. The two lite answers were very similar; the higher-tier model mentioned low-rank matrices and comparable performance. The answers were not identical, and the higher-tier call took substantially longer in this small sample.

### Implementation

Added interactive follow-up questions to `app/ask.py`. Run `uv run python -m app.ask --interactive`, enter follow-up questions, and type `exit` or `quit` to finish. The script creates one Gemini chat and reuses it, so previous turns remain in the conversation history. Unit tests verify chat reuse without making API calls.

### Advanced

Measured response time and provider-reported token counts across two questions and two models. The first question's results are the same three LoRA runs above.

| Question | Model | Response time | Input / output tokens | Result |
|---|---|---:|---:|---|
| What is LoRA? | `gemini-3.5-flash-lite` | 0.63 s, 0.66 s | 14 / 55 on both runs | Both answers defined LoRA correctly. |
| What is LoRA? | `gemini-3.8-flash` | 38.29 s | 14 / 64 | Correct definition; highest observed latency. |
| How does full fine-tuning differ from LoRA? | `gemini-3.5-flash-lite` | 1.44 s | 20 / 63 | Correctly contrasted updating all weights with training LoRA adapters. |
| How does full fine-tuning differ from LoRA? | `gemini-3.8-flash` | Not available | Not available | The API returned HTTP 503 (model busy). |

The course's measured free-quota guidance lists `gemini-3.5-flash-lite` at 15 requests/minute and 500/day, and `gemini-3.8-flash` at 5/minute and roughly 10-20/day, with possible 503 errors. The observed 503 is consistent with the stated availability caveat, but this small experiment does not establish the cause. Higher-tier quota limits make repeated comparisons less practical. These timings are single observations and can vary with network and model load. Temperature was not changed because the course notes that the API may ignore or reject it.

## Japanese Translations of the Generated Answers

These are concise translations of the model responses recorded above.

- Course-specific question (`gemini-3.5-flash-lite`): AIE2026の課題は、一般的には「基礎／Basic（基本概念）」「中級／Application（実践的な応用）」「上級／Mastery（研究と発展）」の3段階に分かれる、と回答しました。これはもっともらしい回答ですが、授業の用語とは異なります。用語集では、Basicは講義内容の復習、Implementationはコードの作成、Advancedは研究と実験を指します。
- LoRA, run 1 (`gemini-3.5-flash-lite`): LoRA（Low-Rank Adaptation）は、元の重みを固定したまま、少数の新しいパラメータを学習することで、大規模な機械学習モデルを効率よくファインチューニングする手法です。これにより、特定のタスクに適応させるための計算量、メモリ、時間を大幅に削減できます。
- LoRA, run 2 (`gemini-3.5-flash-lite`): LoRA（Low-Rank Adaptation）は、元の重みを固定し、少数の追加パラメータだけを学習することで、大規模モデルを効率よくファインチューニングする手法です。これにより、特定のタスクへの適応に必要な計算量、メモリ、時間を大幅に削減できます。
- LoRA, run 3 (`gemini-3.8-flash`): LoRA（Low-Rank Adaptation）は、事前学習済みモデルの重みを固定し、層に小さな学習可能な低ランク行列を追加する、パラメータ効率の高いファインチューニング手法です。学習時のメモリと計算量を大幅に減らしながら、全パラメータのファインチューニングに近い性能を維持できます。
- Full fine-tuning comparison (`gemini-3.5-flash-lite`): フルファインチューニングでは事前学習済みモデルの全パラメータを更新するため、多くの計算資源とメモリが必要です。一方、LoRAは元の重みを固定し、少数の追加の低ランク行列だけを学習するため、メモリ使用量と学習時間を大幅に削減できます。
