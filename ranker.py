
import pandas as pd

from feature_engineering import (
    create_feature_vector
)


def score_candidate(candidate):

    f = create_feature_vector(
        candidate
    )

    skill_score = (
        f["target_skill_matches"] * 8
        + f["avg_proficiency"] * 10
        + min(
            f["avg_endorsements"],
            50
        ) * 0.5
    )

    experience_score = (
        min(
            f["years_experience"],
            15
        ) * 6
        +
        min(
            f["avg_tenure_months"],
            60
        ) * 0.4
    )

    education_score = (
        f["best_education_tier"] * 20
    )

    behavior_score = (
        f["profile_completeness"] * 0.20
        +
        f["response_rate"] * 100 * 0.25
        +
        f["github_score"] * 0.15
        +
        f["interview_completion"] * 100 * 0.20
        +
        min(
            f["saved_by_recruiters"],
            100
        ) * 0.20
    )

    final_score = (
        0.35 * skill_score
        +
        0.25 * experience_score
        +
        0.15 * education_score
        +
        0.25 * behavior_score
    )

    final_score -= (
        f["honeypot_score"] * 15
    )

    return round(
        final_score,
        4
    )


def rank_candidates(candidates):

    rows = []

    for candidate in candidates:

        score = score_candidate(
            candidate
        )

        rows.append({
            "candidate_id":
                candidate[
                    "candidate_id"
                ],
            "score":
                score
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(
        "score",
        ascending=False
    )

    df["rank"] = (
        range(
            1,
            len(df) + 1
        )
    )

    return df


def generate_reasoning(candidate):

    profile = candidate.get(
        "profile",
        {}
    )

    title = profile.get(
        "current_title",
        "Professional"
    )

    years = profile.get(
        "years_of_experience",
        0
    )

    skills = [
        s.get("name")
        for s in candidate.get(
            "skills",
            []
        )[:3]
    ]

    return (
        f"{title} with "
        f"{years:.1f} years experience. "
        f"Strong exposure to "
        f"{', '.join(skills)} "
        f"and positive engagement signals."
    )


def build_submission(
    candidates
):

    ranking = rank_candidates(
        candidates
    )

    lookup = {
        c["candidate_id"]: c
        for c in candidates
    }

    ranking = ranking.head(100)

    ranking["reasoning"] = (
        ranking["candidate_id"]
        .apply(
            lambda x:
            generate_reasoning(
                lookup[x]
            )
        )
    )

    return ranking[
        [
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    ]

