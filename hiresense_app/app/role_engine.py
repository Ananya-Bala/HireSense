from data.role_profiles import role_profiles

CATEGORY_WEIGHTS = {
    "core_skills": 0.4,
    "tooling_skills": 0.25,
    "production_skills": 0.2,
    "research_skills": 0.15
}

def evaluate_role(resume_text: str, role_name: str, similarity_score: float):

    role = role_profiles[role_name]
    resume_lower = resume_text.lower()

    total_weighted_score = 0
    total_coverage = 0
    total_possible = 0
    critical_gap = False

    detailed_matches = {}
    detailed_missing = {}

    for category, skills in role.items():

        matched = []
        missing = []

        for skill in skills:
            if skill.lower() in resume_lower:
                matched.append(skill)
            else:
                missing.append(skill)

        coverage = len(matched) / len(skills) if skills else 0
        weight = CATEGORY_WEIGHTS.get(category, 0)

        total_weighted_score += coverage * weight
        total_coverage += len(matched)
        total_possible += len(skills)

        detailed_matches[category] = matched
        detailed_missing[category] = missing

        # 🚨 Critical gap detection
        if category == "core_skills" and coverage < 0.5:
            critical_gap = True

    # Convert to percentage
    structured_score = total_weighted_score * 100
    similarity_score = similarity_score * 100

    # Combine similarity + structured
    final_score = (0.6 * similarity_score) + (0.4 * structured_score)

    # Apply penalty
    if critical_gap:
        final_score *= 0.75

    skill_coverage_pct = (total_coverage / total_possible) * 100 if total_possible else 0

    # Fit Level
    if final_score >= 75:
        fit_level = "Strong Fit"
        recommendation = "Proceed to technical interview"
    elif final_score >= 55:
        fit_level = "Moderate Fit"
        recommendation = "Consider shortlisting"
    else:
        fit_level = "Weak Fit"
        recommendation = "Not an immediate fit"

    # Confidence Logic
    if final_score >= 75:
        confidence = "High"
    elif final_score >= 55:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "role": role_name,
        "match_score_percentage": round(final_score, 1),
        "fit_level": fit_level,
        "confidence_level": confidence,
        "skill_coverage_percentage": round(skill_coverage_pct, 1),
        "matched_skills": detailed_matches,
        "missing_skills": detailed_missing,
        "recommendation": recommendation
    }