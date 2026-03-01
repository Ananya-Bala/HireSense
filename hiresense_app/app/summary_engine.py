# app/summary_engine.py

def generate_executive_summary(evaluation_data: dict) -> str:
    """
    Deterministic recruiter-grade executive summary.
    No external API required.
    """

    role = evaluation_data.get("role", "the selected role")
    match_score = evaluation_data.get("match_score_percentage", 0)
    strengths = evaluation_data.get("strengths", [])
    risks = evaluation_data.get("risks", [])
    recommendation = evaluation_data.get("recommendation", "Review required")

    # Alignment level
    if match_score >= 75:
        alignment = "strong"
    elif match_score >= 50:
        alignment = "moderate"
    else:
        alignment = "limited"

    # Pick top strengths & risks
    top_strengths = ", ".join(strengths[:3]) if strengths else "core technical areas"
    top_risks = ", ".join(risks[:3]) if risks else "advanced role-specific capabilities"

    summary = (
        f"The candidate demonstrates {alignment} alignment with the {role} role. "
        f"Key strengths include {top_strengths}. "
        f"However, gaps in {top_risks} may impact immediate role performance. "
        f"Overall recommendation: {recommendation}."
    )

    return summary
