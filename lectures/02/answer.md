# Lecture 02 Answers

## Exercises

- **Model and settings:** `Qwen/Qwen3.5-0.8B`; LoRA, no quantization; `lora_r=16`, `lora_alpha=32`, learning rate `0.0002`, 20 epochs, 6 warmup steps, max sequence length 512, seed 42. The adapter had 6,389,760 trainable parameters (0.8421%).
- **Did you run training yourself?** Yes, it was with 20 epochs / 40 steps and 189 seconds of training.
- **Before training:** `format_rate` = 95.2% (20/21); `content_rate` = 38.1% (8/21).
- **After training:** `format_rate` = 100% (21/21); `content_rate` = 95.2% (20/21).
- **Questions that regressed:** None.
- **Failures remaining after training:** One content failure, no broken formats or evidence-backed questions evaded. For “Do office hours require an appointment?”, the model repeated the office-hours schedule and set `needs_review` to `false`; the FAQ did not say whether an appointment was required. This was an assertion without evidence.
- **Knowledge questions (before → after):**

  | Question | In FAQ? | Classification |
  |---|---:|---|
  | When is the final assignment deadline for this course? | No | asserted → asserted |
  | What is the instructor's name? | No | needs_review → needs_review |
  | What is the topic of the next lecture? | No | needs_review → needs_review |
  | When is the assignment deadline? (control) | Yes | asserted → asserted |

  For the absent final-assignment question, the model reused the FAQ's general assignment deadline instead of requesting confirmation. It correctly requested review for the instructor and next-lecture questions both times. Training therefore improved the format and most FAQ answers, but did not make its uncertainty judgment reliable for related, unsupported questions.

- **Training loss:** 1.696 at step 10, 0.073 at step 20, 0.020 at step 30, and 0.015 at step 40.
- **What changed and what stayed the same:** The JSON format became fully compliant, and content accuracy increased from 8/21 to 20/21. The model learned to give clearer answers and handled the held-out FAQ questions better. It still sometimes treated a related FAQ fact as evidence for something the FAQ did not establish.

## Homework

- **Levels attempted:** Basic, Implementation, and Advanced.
- **Settings or data changed:**
  - **Basic:** Changed `lora_r` from 16 to 32; kept `lora_alpha=32`, learning rate `0.0002`, and 20 epochs.
  - **Implementation:** Replaced the course FAQ with a five-item fictional university-library FAQ (5 items: membership, loan_limit, study_rooms, opening_hours, returns). Created paraphrased grounded questions and separate questions about policies absent from the FAQ, then evaluated them with expected answers and `needs_review` labels.
  - **Advanced:** Loaded 116 glossary JSONL training examples and trained for 10 epochs (150 steps), using the rank-32 LoRA settings from the Basic run, learning rate `0.0002`, and 3 warmup steps. The saved training output shows a final logged loss of `0.0771` and an elapsed time of 5 min 20 sec. The three evaluation questions asked about LoRA, QLoRA, and SGD, with SGD designated as absent from the glossary.
- **Results:**

  | Run | Setting / test set | Format rate | Content rate | Final training loss | Training time |
  |---|---|---:|---:|---:|---:|
  | Basic, original | `lora_r=16`, 21 questions | 100% | 95.2% | 0.0148 | 189 s |
  | Basic, changed | `lora_r=32`, 21 questions | 100% | 90.5% | 0.0150 | 187 s |
  | Implementation, before → after | Library FAQ, 7 test questions | 100% → 100% | 0% → 85.7% | 0.0142 after | — |
  | Advanced, glossary, before → after | 116 training examples; 3 questions | 2/3 saved outputs valid JSON → 0/3 |  | 0.0771 | 320 s |

  The rank-32 run had a slightly higher final loss and was about as fast, but its content rate was one answer lower (19/21 instead of 20/21). The implementation test's 85.7% content rate means 6 of 7 answers passed.

  **Advanced observations:** Before SFT, the saved outputs for LoRA and QLoRA were JSON, but the LoRA answer incorrectly set `needs_review` to `true`, and the QLoRA answer called it “Quantum LoRA” and did not explain 4-bit quantization. The saved pre-training SGD output is truncated, so its format and classification cannot be reliably assessed. After SFT, all three answers were plain prose rather than the requested JSON. The LoRA and QLoRA explanations were substantially improved and reflected the glossary; for SGD, which is absent from the glossary, the model still asserted an answer instead of requesting confirmation. Although the notebook defines expected answers for these questions, it does not apply them or calculate advanced `format_rate`/`content_rate`; the advanced assessment above is a manual reading of the saved outputs, not a comparable content score.
- **When fine-tuning is and is not suitable:** Fine-tuning can teach stable terminology, response style, or behavior from repeated examples, but it does not guarantee a required output format across a new dataset or reliable uncertainty judgments for missing facts. Retrieval/search over an authoritative glossary is preferable when answers must track source content and updates: it can surface the relevant text and evidence without retraining. Retrieval does not guarantee perfect accuracy by itself, the source, matching, and final answer still need validation; so unsupported questions should still trigger confirmation rather than an assertion.
