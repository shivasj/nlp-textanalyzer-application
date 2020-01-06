from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from dataaccess import articles
from typing import List, Any, Dict, Optional

router = APIRouter()


class ArticleDetails(BaseModel):
    id: str = Field(..., description="Article Id")
    source: str = Field(..., description="Article Source")
    article_link: str = Field(..., description="Article Link")
    article_date: str = Field(..., description="Article Date")
    article_title: str = Field(..., description="Article Title")
    article_content: str = Field(..., description="Article Content")
    article_dts: int = Field(..., description="Article DTS (epoch)")


@router.get(
    "/articles",
    tags=["Article Data"],
    summary="Gets the articles",
    description="Gets the articles",
    response_description="The list of data objects",
    response_model=List[ArticleDetails]
)
async def source_index(
        summarize: bool = Query(False, description="Summarize article or not"),
        summarize_ratio: float = Query(None, description="Summarization ratio"),
        summarize_word_count: int = Query(None, description="Summarization word count"),
        day: int = Query(None, description="The day to filter by, 0 is today 1 is yesterday"),
        hours: int = Query(None, description="The last 'n' hours to filter by"),
        page_number: int = Query(None, description="The page number to filter by"),
        page_size: int = Query(None, description="The page size to filter by")
):
    if page_number is None:
        page_number = 0

    if summarize_ratio is None:
        summarize_ratio = 0.3

    if page_size is None:
        page_size = 20

    if day is None:
        day = 0

    return await articles.browse(
        summarize=summarize,
        summarize_ratio=summarize_ratio,
        summarize_word_count=summarize_word_count,
        day=day,
        hours=hours,
        page_number=page_number,
        page_size=page_size
    )
