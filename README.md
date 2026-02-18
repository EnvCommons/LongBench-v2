# LongBench v2 Environment

OpenReward environment for the LongBench v2 benchmark: long-context understanding and reasoning evaluation.

## Overview

LongBench v2 contains 503 challenging multiple-choice questions with contexts ranging from 8k to 2M words across six major categories:

- **Single-Document QA** (175 tasks)
- **Multi-Document QA** (125 tasks)
- **Long In-context Learning** (81 tasks)
- **Long-dialogue History Understanding** (39 tasks)
- **Code Repository Understanding** (50 tasks)
- **Long Structured Data Understanding** (33 tasks)

This benchmark tests models' ability to understand and reason over very long contexts, with human expert performance at 53.7% accuracy (15-minute time constraint).

## Splits

### Primary
- **`test`**: All 503 tasks

### Domain-based
- `single-doc-qa`: Single-document question answering (175 tasks)
- `multi-doc-qa`: Multi-document question answering (125 tasks)
- `long-icl`: Long in-context learning (81 tasks)
- `long-dialogue`: Long dialogue history understanding (39 tasks)
- `code-repo`: Code repository understanding (50 tasks)
- `structured-data`: Long structured data understanding (33 tasks)

### Difficulty-based
- `easy`: Easier questions (192 tasks)
- `hard`: Harder questions (311 tasks)

### Length-based
- `short`: Shorter contexts, 8k-30k words (180 tasks)
- `medium`: Medium contexts, 30k-100k words (215 tasks)
- `long`: Longer contexts, 100k-2M words (108 tasks)

## Usage

### Local Testing

```bash
# Download dataset
python -c "from datasets import load_dataset; load_dataset('THUDM/LongBench-v2', split='train').to_parquet('longbench_v2.parquet')"

# Start server
python server.py

# Run test agent (requires OPENAI_API_KEY environment variable)
export OPENAI_API_KEY=your-key-here
python test_agent.py
```

### Docker

```bash
# Build image
docker build -t longbenchv2 .

# Run with local data mount
docker run -v $(pwd)/longbench_v2.parquet:/orwd_data/longbenchv2/longbench_v2.parquet -p 8080:8080 longbenchv2
```

## Tools

- **`submit_answer(answer: str)`**: Submit your answer (A, B, C, or D)
  - Accepts both uppercase (A/B/C/D) and lowercase (a/b/c/d)
  - Returns reward 1.0 for correct, 0.0 for incorrect
  - Ends the episode

## Task Format

Each task consists of:
- **Context**: Very long text (8k to 2M words) - documents, code, structured data, etc.
- **Question**: Multiple-choice question about the context
- **Choices**: Four options (A, B, C, D)
- **Answer**: Single letter indicating the correct choice

## Performance Benchmarks

From the original paper:
- **Human experts** (15-min limit): 53.7% accuracy
- **Direct LLM answering**: ~50.1% accuracy
- **o1-preview**: 57.7% accuracy

## Data Requirements

See [DATA_UPLOAD.md](DATA_UPLOAD.md) for dataset upload instructions. The dataset must be uploaded to OpenReward cloud storage at `/orwd_data/longbenchv2/longbench_v2.parquet`.

## Dataset Source

- **HuggingFace**: [THUDM/LongBench-v2](https://huggingface.co/datasets/THUDM/LongBench-v2)
- **Paper**: [LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks](https://arxiv.org/abs/2412.15204)
- **Project Page**: https://longbench2.github.io
- **Leaderboard**: https://longbench2.github.io/#leaderboard

## Citation

```bibtex
@article{longbenchv2,
  title={LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks},
  author={Yushi Bai and Shangqing Tu and Jiajie Zhang and Hao Peng and Xiaozhi Wang and Xin Lv and Shulin Cao and Jiazheng Xu and Lei Hou and Yuxiao Dong and Jie Tang and Juanzi Li},
  journal={arXiv preprint arXiv:2412.15204},
  year={2024}
}
```

## License

Apache 2.0 (dataset license from HuggingFace)
