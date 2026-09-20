"""Скоринг идеи по четырём критериям. Без сети."""

from __future__ import annotations

from pydantic import BaseModel

MARKET_POINTS = {"niche": 10, "medium": 18, "large": 25, "huge": 30}

CRITERIA = {
    "market": "Market size and demand (max 30)",
    "team": "Team completeness (max 25)",
    "traction": "Paying users and validation (max 25)",
    "competition": "Competitive landscape (max 20)",
}


class Analysis(BaseModel):
    idea: str
    scores: dict[str, int]
    total: int
    verdict: str
    strengths: list[str]
    risks: list[str]


def describe_criteria() -> dict[str, str]:
    return dict(CRITERIA)


def _market_score(market_size: str) -> tuple[int, str]:
    key = market_size.strip().lower()
    if key not in MARKET_POINTS:
        raise ValueError("market_size must be niche, medium, large or huge")
    points = MARKET_POINTS[key]
    note = f"Market is {key} ({points}/30)"
    return points, note


def _team_score(team_size: int) -> tuple[int, str]:
    if team_size < 1:
        raise ValueError("team_size must be >= 1")
    if team_size == 1:
        return 10, "Solo founder: high execution risk"
    if team_size <= 3:
        return 18, "Small team: covers basics"
    if team_size <= 6:
        return 25, "Complete team: product, tech and sales"
    return 20, "Large team: watch the burn rate"


def _traction_score(paying_users: int) -> tuple[int, str]:
    if paying_users < 0:
        raise ValueError("paying_users must be >= 0")
    if paying_users == 0:
        return 5, "No paying users yet: validate demand first"
    if paying_users < 10:
        return 15, "First paying users: promising signal"
    return 25, "Paying users validate demand"


def _competition_score(competitors: int) -> tuple[int, str]:
    if competitors < 0:
        raise ValueError("competitors must be >= 0")
    if competitors == 0:
        return 12, "No visible competitors: check if the market exists"
    if competitors <= 3:
        return 20, "Healthy competition validates the market"
    if competitors <= 10:
        return 15, f"Crowded market: {competitors} competitors"
    return 8, f"Red ocean: {competitors} competitors"


def analyze_idea(
    idea: str,
    market_size: str,
    team_size: int,
    paying_users: int,
    competitors: int,
    fundable_score: int = 85,
    promising_score: int = 60,
) -> Analysis:
    """Оценить идею. Детерминировано."""
    if not idea or not idea.strip():
        raise ValueError("idea must not be empty")
    market_points, market_note = _market_score(market_size)
    team_points, team_note = _team_score(team_size)
    traction_points, traction_note = _traction_score(paying_users)
    competition_points, competition_note = _competition_score(competitors)
    scores = {
        "market": market_points,
        "team": team_points,
        "traction": traction_points,
        "competition": competition_points,
    }
    total = sum(scores.values())
    if total >= fundable_score:
        verdict = "fundable"
    elif total >= promising_score:
        verdict = "promising"
    else:
        verdict = "risky"
    strengths = [
        note
        for note, points, bar in (
            (market_note, market_points, 18),
            (team_note, team_points, 18),
            (traction_note, traction_points, 15),
            (competition_note, competition_points, 15),
        )
        if points >= bar
    ]
    risks = [
        note
        for note, points, bar in (
            (market_note, market_points, 18),
            (team_note, team_points, 18),
            (traction_note, traction_points, 15),
            (competition_note, competition_points, 15),
        )
        if points < bar
    ]
    return Analysis(
        idea=idea.strip(),
        scores=scores,
        total=total,
        verdict=verdict,
        strengths=strengths,
        risks=risks,
    )
