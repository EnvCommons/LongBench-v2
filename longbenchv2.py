from __future__ import annotations

import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field

from openreward.environments import (
    Environment,
    JSONObject,
    TextBlock,
    ToolOutput,
    tool
)

from constants import ENV_PATH


class TaskSpec(BaseModel):
    """Lightweight task specification."""
    task_id: str


class SubmitAnswerInput(BaseModel, extra="forbid"):
    """Input schema for submit_answer tool."""
    answer: str = Field(..., description="Your answer choice: A, B, C, or D")


# Load data at module level with fallback logic
PARQUET_FILE = ENV_PATH / "longbenchv2" / "longbench_v2.parquet"

if PARQUET_FILE.exists():
    # Production path: /orwd_data/longbenchv2/longbench_v2.parquet
    TASKS_DF = pd.read_parquet(PARQUET_FILE)
elif (Path(__file__).parent / "longbench_v2.parquet").exists():
    # Local development fallback
    TASKS_DF = pd.read_parquet(Path(__file__).parent / "longbench_v2.parquet")
else:
    raise FileNotFoundError(
        "longbench_v2.parquet not found. "
        "For local testing, download with: "
        "python -c \"from datasets import load_dataset; load_dataset('THUDM/LongBench-v2', split='train').to_parquet('longbench_v2.parquet')\" "
        "For production, see DATA_UPLOAD.md"
    )


class LongBenchV2(Environment):
    """
    LongBench v2: Long-context understanding and reasoning benchmark.

    503 multiple-choice questions with contexts from 8k to 2M words,
    spanning 6 task categories:
    - Single-Document QA (175 tasks)
    - Multi-Document QA (125 tasks)
    - Long In-context Learning (81 tasks)
    - Long-dialogue History Understanding (39 tasks)
    - Code Repository Understanding (50 tasks)
    - Long Structured Data Understanding (33 tasks)

    Evaluation uses exact match on answer letters (A/B/C/D).
    Human expert baseline: 53.7% (15-min limit)
    """

    def __init__(self, task_spec: JSONObject, secrets: dict[str, str] = {}) -> None:
        super().__init__(task_spec)
        self.validated = TaskSpec.model_validate(task_spec)

        # Load task from DataFrame
        task_rows = TASKS_DF[TASKS_DF["_id"] == self.validated.task_id]
        if len(task_rows) == 0:
            raise ValueError(
                f"Task ID '{self.validated.task_id}' not found in dataset. "
                f"Available task IDs: {TASKS_DF['_id'].head().tolist()}"
            )
        task_row = task_rows.iloc[0]

        self.task_id = task_row["_id"]
        self.domain = task_row["domain"]
        self.sub_domain = task_row["sub_domain"]
        self.difficulty = task_row["difficulty"]
        self.length = task_row["length"]
        self.question = task_row["question"]
        self.choice_A = task_row["choice_A"]
        self.choice_B = task_row["choice_B"]
        self.choice_C = task_row["choice_C"]
        self.choice_D = task_row["choice_D"]
        self.correct_answer = task_row["answer"]
        self.context = task_row["context"]

    @classmethod
    def list_splits(cls) -> list[str]:
        """Return all available splits."""
        return [
            "test",
            # Domain-based splits
            "single-doc-qa", "multi-doc-qa", "long-icl",
            "long-dialogue", "code-repo", "structured-data",
            # Difficulty-based splits
            "easy", "hard",
            # Length-based splits
            "short", "medium", "long"
        ]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        """Return task specifications for the given split."""
        df = TASKS_DF

        if split == "test":
            filtered = df
        elif split in ["easy", "hard"]:
            filtered = df[df["difficulty"] == split]
        elif split in ["short", "medium", "long"]:
            filtered = df[df["length"] == split]
        else:
            # Domain mapping
            domain_map = {
                "single-doc-qa": "Single-Document QA",
                "multi-doc-qa": "Multi-Document QA",
                "long-icl": "Long In-context Learning",
                "long-dialogue": "Long-dialogue History Understanding",
                "code-repo": "Code Repository Understanding",
                "structured-data": "Long Structured Data Understanding"
            }
            if split in domain_map:
                filtered = df[df["domain"] == domain_map[split]]
            else:
                return []  # Unknown split

        return [{"task_id": row["_id"]} for _, row in filtered.iterrows()]

    async def get_prompt(self) -> list[TextBlock]:
        """Generate the task prompt with context, question, and choices."""
        prompt = f"""[CONTEXT]
{self.context}

[QUESTION]
{self.question}

[CHOICES]
A) {self.choice_A}
B) {self.choice_B}
C) {self.choice_C}
D) {self.choice_D}

Please analyze the context carefully and submit your answer using the submit_answer tool."""

        return [TextBlock(text=prompt)]

    @tool
    async def submit_answer(self, params: SubmitAnswerInput) -> ToolOutput:
        """Submit your final answer (A, B, C, or D). This ends the episode."""

        submitted = params.answer.strip().upper()
        expected = self.correct_answer.strip().upper()

        # Validate input
        if submitted not in {"A", "B", "C", "D"}:
            return ToolOutput(
                blocks=[TextBlock(text="❌ Invalid answer. Please submit A, B, C, or D.")],
                metadata={
                    "task_id": self.task_id,
                    "submitted": params.answer,
                    "valid": False
                },
                reward=0.0,
                finished=True
            )

        correct = (submitted == expected)
        reward = 1.0 if correct else 0.0

        if correct:
            message = "✅ Correct!"
        else:
            message = f"❌ Incorrect. The correct answer was {expected}."

        return ToolOutput(
            blocks=[TextBlock(text=message)],
            metadata={
                "task_id": self.task_id,
                "submitted": submitted,
                "expected": expected,
                "correct": correct,
                "domain": self.domain,
                "difficulty": self.difficulty,
                "length": self.length
            },
            reward=reward,
            finished=True
        )
