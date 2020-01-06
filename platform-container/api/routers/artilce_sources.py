from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from dataaccess import article_sources
from typing import List, Any, Dict, Optional

router = APIRouter()

class ArticleSourceDetails(BaseModel):
    source: str = Field(..., description="Article Source")
    url: str = Field(..., description="Article Link")
    link_selector: str = Field(..., description="Article Date")
    time_selector: str = Field(..., description="Article Title")
    title_selector: str = Field(..., description="Article Content")
    content_selector: str = Field(..., description="Article Content")
    enabled: bool = Field(..., description="Article DTS (epoch)")


@router.get(
    "/article_sources",
    tags=["Article Source"],
    summary="Gets the article sources",
    description="Gets the article sources",
    response_description="The list of data objects",
    response_model=List[ArticleSourceDetails]
)
async def source_index():

    return await article_sources.browse()
