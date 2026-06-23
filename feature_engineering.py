
import re
import numpy as np
from datetime import datetime

PROFICIENCY_MAP = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
    "expert": 4
}

TARGET_SKILLS = {
    "python",
    "machine learning",
    "deep learning",
    "nlp",
    "llm",
    "rag",
    "embeddings",
    "vector databases",
    "milvus",
    "pinecone",
    "faiss",
    "langchain",
    "search",
    "ranking",
    "retrieval",
    "recommendation systems",
    "sql",
    "pytorch",
    "tensorflow",
    "aws",
    "gcp",
    "docker",
    "kubernetes"
}


def safe_get(obj, *keys, default=None):
    cur = obj
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            return default
    return cur if cur is not None else default


def normalize(value, min_val, max_val):
    value = max(min_val, min(value, max_val))
    return (value - min_val) / (max_val - min_val + 1e-9)


def extract_skill_features(candidate):

    skills = candidate.get("skills", [])

    skill_names = []
    prof_scores = []
    endorsements = []
    durations = []

    target_skill_matches = 0

    for s in skills:

        name = s.get("name", "").lower().strip()
        skill_names.append(name)

        prof_scores.append(
            PROFICIENCY_MAP.get(
                s.get("proficiency", "").lower(),
                0
            )
        )

        endorsements.append(
            s.get("endorsements", 0)
        )

        durations.append(
            s.get("duration_months", 0)
        )

        for target in TARGET_SKILLS:
            if target in name:
                target_skill_matches += 1

    return {
        "num_skills": len(skills),
        "avg_proficiency": np.mean(prof_scores) if prof_scores else 0,
        "avg_endorsements": np.mean(endorsements) if endorsements else 0,
        "avg_skill_duration": np.mean(durations) if durations else 0,
        "target_skill_matches": target_skill_matches
    }


def extract_experience_features(candidate):

    profile = candidate.get("profile", {})
    career = candidate.get("career_history", [])

    years_exp = profile.get(
        "years_of_experience",
        0
    )

    durations = [
        c.get("duration_months", 0)
        for c in career
    ]

    job_hops = max(0, len(career) - 1)

    avg_tenure = (
        np.mean(durations)
        if durations else 0
    )

    return {
        "years_experience": years_exp,
        "job_hops": job_hops,
        "avg_tenure_months": avg_tenure
    }


def extract_education_features(candidate):

    education = candidate.get(
        "education",
        []
    )

    tier_map = {
        "tier_1": 4,
        "tier_2": 3,
        "tier_3": 2,
        "tier_4": 1
    }

    best_tier = 0

    for edu in education:
        best_tier = max(
            best_tier,
            tier_map.get(
                edu.get("tier", "").lower(),
                0
            )
        )

    return {
        "best_education_tier": best_tier,
        "education_count": len(education)
    }


def extract_behavior_features(candidate):

    sig = candidate.get(
        "redrob_signals",
        {}
    )

    return {
        "profile_completeness":
            sig.get(
                "profile_completeness_score",
                0
            ),

        "response_rate":
            sig.get(
                "recruiter_response_rate",
                0
            ),

        "response_time":
            sig.get(
                "avg_response_time_hours",
                0
            ),

        "github_score":
            max(
                0,
                sig.get(
                    "github_activity_score",
                    0
                )
            ),

        "saved_by_recruiters":
            sig.get(
                "saved_by_recruiters_30d",
                0
            ),

        "interview_completion":
            sig.get(
                "interview_completion_rate",
                0
            ),

        "offer_acceptance":
            max(
                0,
                sig.get(
                    "offer_acceptance_rate",
                    0
                )
            ),

        "search_appearance":
            sig.get(
                "search_appearance_30d",
                0
            )
    }


def honeypot_score(candidate):

    score = 0

    profile = candidate.get(
        "profile",
        {}
    )

    skills = candidate.get(
        "skills",
        []
    )

    sig = candidate.get(
        "redrob_signals",
        {}
    )

    years = profile.get(
        "years_of_experience",
        0
    )

    expert_count = 0

    for s in skills:

        prof = (
            s.get(
                "proficiency",
                ""
            )
            .lower()
        )

        duration = s.get(
            "duration_months",
            0
        )

        if prof == "expert":
            expert_count += 1

        if prof == "expert" and duration < 6:
            score += 1

    if expert_count > 10:
        score += 2

    if years < 2 and expert_count > 8:
        score += 2

    signup = sig.get(
        "signup_date"
    )

    active = sig.get(
        "last_active_date"
    )

    try:
        if signup and active:
            s = datetime.fromisoformat(signup)
            a = datetime.fromisoformat(active)

            if s > a:
                score += 3

    except Exception:
        pass

    return score


def create_feature_vector(candidate):

    features = {}

    features.update(
        extract_skill_features(candidate)
    )

    features.update(
        extract_experience_features(candidate)
    )

    features.update(
        extract_education_features(candidate)
    )

    features.update(
        extract_behavior_features(candidate)
    )

    features["honeypot_score"] = (
        honeypot_score(candidate)
    )

    return features

