from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from dataaccess import article_sources
from typing import List, Any, Dict, Optional

router = APIRouter()

class ArticleSourceDetails(BaseModel):
    source: str = Field(..., description="Article Source")
    url: str = Field(..., description="Article Source Link")
    link_selector: str = Field(..., description="Link CSS Selector")
    time_selector: str = Field(..., description="Time CSS Selector")
    title_selector: str = Field(..., description="Title CSS Selector")
    content_selector: str = Field(..., description="Content CSS Selector")
    enabled: bool = Field(..., description="Article Source Enabled")


@router.get(
    "/article_sources",
    tags=["Article Source"],
    summary="Gets the article sources",
    description="Gets the article sources",
    response_description="The list of data objects",
    response_model=List[ArticleSourceDetails]
)
async def article_source_index():

    return await article_sources.browse()


@router.post(
    "/article_sources",
    tags=["Article Source"],
    summary="Create a new Article Source",
    description="Create a new Article Source",
    response_description="The created data",
    response_model=ArticleSourceDetails
)
async def article_source_create(
        article_source: ArticleSourceDetails
):
    article_source = await article_sources.create(
        source=article_source.source,
        url=article_source.url,
        link_selector=article_source.link_selector,
        time_selector=article_source.time_selector,
        title_selector=article_source.title_selector,
        content_selector=article_source.content_selector,
        enabled=article_source.enabled
    )

    return article_source
