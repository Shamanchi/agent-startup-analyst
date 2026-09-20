"""Эндпоинты анализа идей."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.services.scoring import Analysis, analyze_idea, describe_criteria

router = APIRouter()


class AnalyzeRequest(BaseModel):
    idea: str = Field(min_length=1, max_length=2000)
    market_size: Literal["niche", "medium", "large", "huge"]
    team_size: int = Field(ge=1, le=1000)
    paying_users: int = Field(ge=0, le=10_000_000)
    competitors: int = Field(ge=0, le=10000)


@router.get("/criteria")
async def criteria() -> dict:
    return {"criteria": describe_criteria()}


@router.post("/analyze", response_model=Analysis)
async def analyze(
    request: AnalyzeRequest,
    settings: Settings = Depends(get_settings),
) -> Analysis:
    try:
        return analyze_idea(
            request.idea,
            request.market_size,
            request.team_size,
            request.paying_users,
            request.competitors,
            fundable_score=settings.fundable_score,
            promising_score=settings.promising_score,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
