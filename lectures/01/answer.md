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
| How does full fine-tuning differ from LoRA? | `gemini-3.8-flash` | First invocation returned 503; next invocation succeeded in 103.93 s | 20 / 54 on the successful invocation | Correctly contrasted full parameter updates with LoRA adapters. |

The course's measured free-quota guidance lists `gemini-3.5-flash-lite` at 15 requests/minute and 500/day, and `gemini-3.8-flash` at 5/minute and roughly 10-20/day, with possible 503 errors. Google's API error reference defines 503 as the service being temporarily overloaded or down and recommends waiting and retrying with exponential backoff. The troubleshooting guide also says the Python SDK retries transient errors automatically by default. Our next invocation succeeded, which supports a transient availability problem, but does not identify the cause of the first failure or prove that a quota was exhausted. The 103.93-second measurement includes the SDK call and may include internal retry delays; the SDK does not expose per-attempt timings in this script.

To explore temperature, I made one additional request to `gemini-3.5-flash-lite` with `temperature=0.2` and the same LoRA question. The installed SDK accepts the field, and the API accepted the request: 0.93 seconds, 14 input / 70 output tokens. This single successful request cannot show whether the model honored the value or whether it caused the longer answer. The current Gemini 3 guide strongly recommends keeping temperature at its default `1.0`; it warns that values below 1.0 can lead to unexpected behavior or degraded performance, especially on complex reasoning tasks. That is more specific than saying the parameter is always deprecated, ignored, or rejected. The course slide's deprecation note and the current documentation appear to differ, so I would follow the course's instruction to record behavior as observed and avoid relying on temperature for this comparison.

These are small-sample observations: latency varies with network and model load, and outputs are stochastic. The quota figures above are the course's measured guidance, not limits verified by this experiment.

References checked on 2026-10-26:

- [Gemini API errors](https://ai.google.dev/gemini-api/docs/api-errors): 503 means temporary service overload or outage; retry with exponential backoff.
- [Gemini API troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting): SDK automatic retry behavior and backoff guidance.
- [Gemini 3 guide](https://ai.google.dev/gemini-api/docs/gemini-3): recommends the default temperature of 1.0 and cautions against lowering it.

## Japanese Translations of the Generated Answers

The translations below follow the same paragraph and list structure as the corresponding model answers.

### Exercise: Course-Specific Question (`gemini-3.5-flash-lite`)

AIE2026コース（Advanced Artificial Intelligence and Engineering／AI Engineering 2026プログラム）で一般的に用いられる構成に基づくと、宿題や課題は、学習ペースや理解の深さに応じられるよう、通常は次の3段階に分類されます。

1. **レベル1: Foundation / Basic（基礎／基本概念）**
	- **重点:** 基本的な概念、構文、基本的な実装を理解すること。
	- **目標:** ガイド付き演習、標準的な小テスト、簡単なコーディング課題を通じて、受講者が講義の中心的な内容を理解したことを確認します。
2. **レベル2: Intermediate / Application（中級／応用）**
	- **重点:** 概念を実際の状況に応用し、既存のモデルを変更し、問題を解決すること。
	- **目標:** 独自コードの作成、データセットの処理、中程度の難易度のエンジニアリング課題の解決を求め、理論と実践を結び付けます。
3. **レベル3: Advanced / Mastery（上級／熟達）**
	- **重点:** 最適化、例外的なケース、自由度の高い課題を深く探究すること。
	- **目標:** より高い熟達を目指す受講者向けです。高度なアーキテクチャ調整、研究論文の再現、複雑で明確な答えのない課題に取り組むことが含まれます。

（注: シラバスで「Core、Practice、Challenge」など別の用語が使われている場合は、それに合わせて正確に説明できます。）

This answer sounded plausible but did not match the course glossary: Basic means reviewing lecture content, Implementation means writing code, and Advanced means research and experimentation.

### Basic: "What Is LoRA?"

**Run 1 (`gemini-3.5-flash-lite`):**

LoRA（Low-Rank Adaptation）は、元の重みを固定し、はるかに少数の新しいパラメータを学習することで、大規模な機械学習モデルを効率的にファインチューニングする手法です。これにより、モデルを特定のタスクに適応させるために必要な計算能力、メモリ、時間を大幅に削減できます。

**Run 2 (`gemini-3.5-flash-lite`):**

LoRA（Low-Rank Adaptation）は、元の重みを固定し、はるかに少数の追加パラメータを学習することで、大規模な機械学習モデルを効率的にファインチューニングする手法です。これにより、モデルを特定のタスクに適応させるために必要な計算能力、メモリ、時間を大幅に削減できます。

**Run 3 (`gemini-3.8-flash`):**

LoRA（Low-Rank Adaptation）は、事前学習済み大規模言語モデルの重みを固定し、その各層に小さな学習可能な低ランク行列を追加する、パラメータ効率の高いファインチューニング手法です。この方法では、学習時のメモリと計算量を大幅に削減しながら、フルファインチューニングに匹敵する性能を維持できます。

### Advanced: Full Fine-Tuning Compared with LoRA

**`gemini-3.5-flash-lite`:**

フルファインチューニングでは、事前学習済みモデルの全パラメータを更新するため、計算コストが高く、大量のメモリが必要になります。これに対し、LoRA（Low-Rank Adaptation）は元のモデルの重みを固定し、少数の追加の低ランク行列だけを学習するため、メモリ使用量と学習時間を大幅に削減できます。

**`gemini-3.8-flash` (successful retry):**

フルファインチューニングではモデルの全パラメータを更新するため、多くの計算資源が必要になり、重み一式を新たに作成します。これに対し、LoRAは元のモデルを固定し、小さな低ランクのアダプター行列だけを学習するため、メモリ使用量と保存容量を大幅に削減できます。

### Advanced: LoRA with `temperature=0.2`

**`gemini-3.5-flash-lite`:**

LoRA（Low-Rank Adaptation）は、元のモデルの重みを固定し、新しいパラメータのごく一部だけを学習することで、大規模AIモデルのファインチューニングをはるかに高速かつ効率的に行う手法です。巨大なネットワーク全体を更新する代わりに、小さな「ランク分解」行列を追加して学習するため、高い性能を維持しながらメモリ使用量を大幅に削減できます。
