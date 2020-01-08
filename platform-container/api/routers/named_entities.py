from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from dataaccess import named_entities
from typing import List, Any, Dict, Optional

router = APIRouter()

@router.get(
    "/browse_by_entity",
    tags=["Entity"],
    summary="Gets the Entity counts",
    description="Gets the Entity counts",
    response_description="The list of data objects",
    response_model=List[Dict[str, Any]]
)
async def browse_by_entity(
        entity: str = Query(..., description="The entity to filter by"),
        day: int = Query(..., description="The day to filter by, 0 is today 1 is yesterday"),
        hours: int = Query(..., description="The last 'n' hours to filter by"),
        top: int = Query(..., description="The top 'n' to filter by")):

    if day is None:
        day = 0

    return await named_entities.browse_by_entity(entity=entity,day=day,hours=hours,top=top)
