
import json
import pandas as pd

from ranker import (
    build_submission
)

INPUT_FILE = (
    "dataset/candidates.jsonl"
)

OUTPUT_FILE = (
    "dataset/submission.csv"
)

def load_candidates():

    candidates = []

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            candidates.append(
                json.loads(line)
            )

    return candidates

def main():

    candidates = (
        load_candidates()
    )

    submission = (
        build_submission(
            candidates
        )
    )

    submission.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Saved {OUTPUT_FILE}"
    )

if __name__ == "__main__":
    main()

