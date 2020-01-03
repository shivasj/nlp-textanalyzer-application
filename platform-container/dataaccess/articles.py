import os
import numpy as np
import pandas as pd

from typing import Any, Dict, List

from dataaccess.session import database

async def browse(
        *,
        page_number: int = 0,
        page_size: int = 20
) -> List[Dict[str, Any]]:
    """
    Retrieve a list of rows from the database
    """


    sql = "select * from articles"
    sql += " order by article_dts desc"
    sql += " limit "+str(page_size)
    sql += " offset "+str(page_number * page_size)

    print(sql)
    result = await database.fetch_all(sql, values={})

    return [dict(row) for row in result]


def create(*,
                id: str,
                source: str,
                article_link: str,
                article_date: str,
                article_title: str,
                article_content: str,
                article_dts: int) -> Dict[str, Any]:
    """
    Create a row in db. Returns the created record as a dict.
    """

    # Set the values
    values = {
        "id": id,
        "source": source,
        "article_link": article_link,
        "article_date": article_date,
        "article_title": article_title,
        "article_content": article_content,
        "article_dts": article_dts
    }

    # Generate the field and values list
    field_list = ", ".join(values.keys())
    param_list = ", ".join("?" for key in values.keys())
    value_tuple = [value for key,value in values.items()]
    value_tuple = tuple(value_tuple)
    print(field_list,param_list,value_tuple)

    sql = f"""
        INSERT OR REPLACE INTO articles (
            {field_list}
        ) VALUES (
            {param_list}
        );
    """

    print(sql)
    database.execute(sql,value_tuple)
    database.commit()

    return values
