import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from typing import Any, Dict, List

from dataaccess.session import database


async def browse() -> List[Dict[str, Any]]:
    """
    Retrieve a list of rows from the database
    """

    sql = "select * from article_sources where 1=1"

    print(sql)
    rows = pd.read_sql_query(sql, database)

    return rows.to_dict('records')


async def create(*,
           source: str,
           url: str,
           link_selector: str,
           time_selector: str,
           title_selector: str,
           content_selector: str,
           enabled:bool) -> Dict[str, Any]:
    """
    Create a row in db. Returns the created record as a dict.
    """

    # Set the values
    values = {
        "source": source,
        "url": url,
        "link_selector": link_selector,
        "time_selector": time_selector,
        "title_selector": title_selector,
        "content_selector": content_selector,
        "enabled": enabled
    }

    # Generate the field and values list
    field_list = ", ".join(values.keys())
    param_list = ", ".join("?" for key in values.keys())
    value_tuple = [value for key,value in values.items()]
    value_tuple = tuple(value_tuple)
    print(field_list,param_list,value_tuple)

    sql = f"""
        INSERT OR REPLACE INTO article_sources (
            {field_list}
        ) VALUES (
            {param_list}
        );
    """

    print(sql)
    database.execute(sql,value_tuple)
    database.commit()

    return values

