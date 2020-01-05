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
        last_n_hours: int = Query(None, description="The last 'n' hours to filter by"),
        page_number: int = Query(None, description="The page number to filter by"),
        page_size: int = Query(None, description="The page size to filter by")
):
    return await articles.browse(
        last_n_hours=last_n_hours,
        page_number=page_number,
        page_size=page_size
    )
