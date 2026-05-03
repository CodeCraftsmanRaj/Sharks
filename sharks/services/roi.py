from __future__ import annotations

from sharks.schemas import RoiIn


def roi_estimate(payload: RoiIn) -> dict[str, object]:
    salary_benchmarks = {
        "United States": 120000,
        "Canada": 85000,
        "United Kingdom": 70000,
        "Germany": 65000,
        "India": 1200000,
    }
    annual_salary = salary_benchmarks.get(payload.country, 60000)
    total_cost = payload.tuition_cost + (payload.living_cost_per_year * payload.duration_years)
    monthly_salary = annual_salary / 12
    payback_months = round(total_cost / max(monthly_salary, 1), 1)
    roi_ratio = round((annual_salary * payload.duration_years) / max(total_cost, 1), 2)
    return {
        "expected_annual_salary": annual_salary,
        "total_education_cost": round(total_cost, 2),
        "estimated_payback_months": payback_months,
        "roi_ratio": roi_ratio,
    }
