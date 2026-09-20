"""Unit-тесты скоринга: без сети, детерминированы."""

import pytest

from app.services.scoring import analyze_idea, describe_criteria


def test_fundable_case() -> None:
    result = analyze_idea("CRM for dentists", "large", 4, 12, 3)
    assert result.scores == {"market": 25, "team": 25, "traction": 25, "competition": 20}
    assert result.total == 95
    assert result.verdict == "fundable"
    assert len(result.strengths) == 4
    assert result.risks == []


def test_risky_case() -> None:
    result = analyze_idea("Yet another chat", "niche", 1, 0, 50)
    assert result.total == 10 + 10 + 5 + 8
    assert result.verdict == "risky"
    assert len(result.risks) == 4


def test_promising_middle() -> None:
    result = analyze_idea("Dev tool", "medium", 2, 5, 2)
    assert result.total == 18 + 18 + 15 + 20
    assert result.verdict == "promising"


def test_bad_input_rejected() -> None:
    with pytest.raises(ValueError):
        analyze_idea("   ", "large", 2, 0, 0)
    with pytest.raises(ValueError):
        analyze_idea("Idea", "cosmic", 2, 0, 0)
    with pytest.raises(ValueError):
        analyze_idea("Idea", "large", 0, 0, 0)


def test_criteria_described() -> None:
    assert set(describe_criteria()) == {"market", "team", "traction", "competition"}
