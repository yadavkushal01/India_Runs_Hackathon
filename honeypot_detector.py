
from datetime import datetime

def detect_honeypot(candidate):

    flags = []
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

    years_exp = profile.get(
        "years_of_experience",
        0
    )

    expert_count = 0

    for skill in skills:

        proficiency = (
            skill.get(
                "proficiency",
                ""
            )
            .lower()
        )

        duration = skill.get(
            "duration_months",
            0
        )

        if proficiency == "expert":
            expert_count += 1

        if (
            proficiency == "expert"
            and duration < 3
        ):
            flags.append(
                "expert_without_usage"
            )
            score += 2

    if expert_count > 10:
        flags.append(
            "too_many_expert_skills"
        )
        score += 3

    if (
        years_exp < 2
        and expert_count > 8
    ):
        flags.append(
            "junior_expert_conflict"
        )
        score += 4

    signup = sig.get(
        "signup_date"
    )

    active = sig.get(
        "last_active_date"
    )

    try:

        if signup and active:

            signup_dt = (
                datetime.fromisoformat(
                    signup
                )
            )

            active_dt = (
                datetime.fromisoformat(
                    active
                )
            )

            if signup_dt > active_dt:

                flags.append(
                    "date_impossible"
                )

                score += 5

    except:
        pass

    return {
        "honeypot_score": score,
        "flags": flags
    }
