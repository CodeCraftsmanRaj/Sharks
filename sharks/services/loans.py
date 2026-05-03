from __future__ import annotations

from sharks.schemas import LoanIn


def loan_eligibility(payload: LoanIn) -> dict[str, object]:
    score = 0
    score += 35 if payload.marks >= 85 else 25 if payload.marks >= 70 else 10
    score += 25 if payload.family_income >= 1_500_000 else 15 if payload.family_income >= 800_000 else 5
    score += 20 if payload.budget <= 2_500_000 else 10 if payload.budget <= 5_000_000 else 5
    score = min(95, score)

    eligible_amount = min(payload.budget * 1.1, 7_000_000)
    if score >= 70:
        status = "eligible"
        offers = [
            {"name": "Student Starter Loan", "loan_amount": round(eligible_amount, 2), "tenure_years": 10},
            {"name": "Co-applicant Boost Loan", "loan_amount": round(eligible_amount * 1.2, 2), "tenure_years": 12},
        ]
    elif score >= 50:
        status = "pre-approved"
        offers = [{"name": "Indicative Offer", "loan_amount": round(eligible_amount * 0.75, 2), "tenure_years": 8}]
    else:
        status = "needs-review"
        offers = []

    return {"status": status, "score": score, "offers": offers}
