from __future__ import annotations

from typing import Any

from sharks.schemas import StudentProfile


def recommend_options(profile: StudentProfile) -> dict[str, Any]:
    marks = profile.marks or 0
    budget = profile.budget or 0
    course = (profile.target_course or "").lower()

    if budget >= 3_500_000 or marks >= 85:
        countries = ["United States", "Canada", "United Kingdom"]
    elif budget >= 1_500_000:
        countries = ["Germany", "Ireland", "Australia"]
    else:
        countries = ["India", "Germany", "Italy"]

    course_suggestions = ["Computer Science", "Data Science", "Business Analytics", "Finance", "Management"]
    if "ai" in course or "data" in course:
        course_suggestions.insert(0, "Artificial Intelligence")

    university_tier = "high reach" if marks >= 85 else "moderate" if marks >= 70 else "safe"
    return {
        "countries": countries,
        "courses": course_suggestions[:4],
        "university_tier": university_tier,
        "suggested_budget_band": "high" if budget >= 3_500_000 else "mid" if budget >= 1_500_000 else "low",
    }
