from __future__ import annotations

from sharks.schemas import StudentProfile


def admission_probability(profile: StudentProfile) -> dict[str, object]:
    marks = profile.marks or 0
    work_experience = profile.work_experience or 0
    budget = profile.budget or 0

    score = 20
    score += min(45, marks * 0.45)
    score += min(15, work_experience * 3)
    score += 10 if budget >= 1_500_000 else 5 if budget >= 800_000 else 0
    score = round(min(95, score), 1)

    if score >= 80:
        band = "high"
    elif score >= 60:
        band = "moderate"
    else:
        band = "low"

    return {"score": score, "band": band, "note": "Rule-based demo score for hackathon prototype"}
