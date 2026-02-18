# Data Upload Requirements for LongBenchV2

## Overview
This environment requires the LongBench-v2 dataset (503 long-context multiple-choice questions) to be uploaded to OpenReward cloud storage.

## Directory Structure
```
/orwd_data/longbenchv2/
└── longbench_v2.parquet (162 MB)
```

## File Description
- **longbench_v2.parquet**: Complete LongBench v2 dataset with 503 tasks
  - Contexts: 8k to 2M words
  - Categories: Single-doc QA, Multi-doc QA, Long ICL, Long dialogue, Code repos, Structured data
  - Fields: _id, domain, sub_domain, difficulty, length, question, choice_A/B/C/D, answer, context

## How to Generate
```python
from datasets import load_dataset

# Download from HuggingFace
dataset = load_dataset('THUDM/LongBench-v2', split='train')

# Save as parquet
dataset.to_parquet('longbench_v2.parquet')
```

Or via command line:
```bash
python -c "from datasets import load_dataset; load_dataset('THUDM/LongBench-v2', split='train').to_parquet('longbench_v2.parquet')"
```

## Upload Instructions
1. Generate the parquet file using the script above
2. Upload to your OpenReward namespace at https://openreward.ai
3. Upload to path: `/orwd_data/longbenchv2/longbench_v2.parquet`

## Dataset Statistics
- **Total tasks**: 503
- **Downloaded size**: 465 MB
- **Parquet size**: 162 MB
- **Context lengths**: 8k to 2M words (majority <128k)

## Task Distribution
- **Single-Document QA**: 175 tasks
- **Multi-Document QA**: 125 tasks
- **Long In-context Learning**: 81 tasks
- **Long-dialogue History Understanding**: 39 tasks
- **Code Repository Understanding**: 50 tasks
- **Long Structured Data Understanding**: 33 tasks

## Dataset Source
- **HuggingFace**: [THUDM/LongBench-v2](https://huggingface.co/datasets/THUDM/LongBench-v2)
- **Paper**: [LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks](https://arxiv.org/abs/2412.15204)
- **Project Page**: https://longbench2.github.io
- **License**: Apache 2.0
