# LongBench-v2

[![OpenReward Badge](https://img.shields.io/badge/%E2%AD%90%20OpenReward-Environment-f7e6cc)](https://openreward.ai/GeneralReasoning/LongBenchV2)
[![Hugging Face Badge](https://img.shields.io/badge/Hugging%20Face-Dataset-orange)](https://huggingface.co/datasets/THUDM/LongBench-v2)

## Description

LongBench-v2 is an environment for evaluating long-context understanding and reasoning. Based on the LongBench v2 benchmark from THUDM, agents are given long documents (8K–2M words) and must answer multiple-choice questions (A/B/C/D) that require deep comprehension across six task domains.

## Capabilities

- **Long-context document comprehension** (8K–2M words)
- **Multiple-choice reasoning** over extended text
- **Cross-domain understanding** including QA, code, dialogue, structured data, and in-context learning

## Compute Requirements

Agents are given a standard environment with no sandbox or file system access.

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Tasks

One primary split: **test** (503 tasks).

Also available as domain-based splits:
- single-doc-qa (175 tasks)
- multi-doc-qa (125 tasks)
- long-icl (81 tasks)
- long-dialogue (39 tasks)
- code-repo (50 tasks)
- structured-data (33 tasks)

Tasks span three difficulty levels:
- easy: 192 tasks
- hard: 311 tasks

Tasks span three length categories:
- short (8K–30K words): 180 tasks
- medium (30K–100K words): 215 tasks
- long (100K–2M words): 108 tasks

## Reward Structure

Single-turn evaluation. Agents submit an answer choice (A/B/C/D) via the `submit_answer` tool. Reward is deterministic based on exact match:
- **1.0** if the submitted answer is correct
- **0.0** if the submitted answer is incorrect

## Data

longbench_v2.parquet (162 MB) sourced from [HuggingFace THUDM/LongBench-v2](https://huggingface.co/datasets/THUDM/LongBench-v2). Data is stored on the OpenReward platform.

## Tools

**`submit_answer`**: Submit an answer choice (A, B, C, or D) to the multiple-choice question. This is the only tool available and completes the task.

## Time Horizon

Single-turn evaluation.

## Environment Difficulty

Tasks require deep comprehension of documents spanning 8K to 2M words. The benchmark is designed to be challenging for both humans and LLMs, with context lengths that push the limits of current model architectures.

## Other Environment Requirements

There are no further environment requirements; LongBench-v2 works out of the box with the OpenReward endpoint without any external API keys.

## Safety

Agents in LongBench-v2 answer multiple-choice questions about long documents in a standard environment. The environment does not present direct safety risks.

## Citations

```bibtex
@article{bai2024longbenchv2,
  title={LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks},
  author={Bai, Yushi and others},
  journal={arXiv preprint arXiv:2412.15204},
  year={2024}
}
```
