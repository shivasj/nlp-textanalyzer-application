import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from typing import Any, Dict, List
from gensim.summarization import summarize as summarize_text

from dataaccess.session import database

async def browse(
        *,
        summarize: bool = False,
        summarize_ratio: float = 0.3,
        summarize_word_count: int = None,
        day: int = 0,
        hours: int = None,
        page_number: int = 0,
        page_size: int = 20
) -> List[Dict[str, Any]]:
    """
    Retrieve a list of rows from the database
    """


    sql = "select * from articles where 1=1"

    if hours is not None:
        today = datetime.today() + timedelta(days=1)
        end_time = datetime(today.year, today.month, today.day, 0, 0) - timedelta(days=day)
        start_time = end_time - timedelta(hours=hours)


        sql += " and article_dts >= "+ str(start_time.timestamp())
        sql += " and article_dts <= " + str(end_time.timestamp())

    sql += " order by article_dts desc"

    if hours is None:
        sql += " limit "+str(page_size)
        sql += " offset "+str(page_number * page_size)

    print(sql)
    rows = pd.read_sql_query(sql, database)

    # Summarize
    if summarize:
        def generate_summary(text):
            return summarize_text(text, ratio=summarize_ratio, word_count=summarize_word_count)

        rows['article_content'] = rows['article_content'].apply(generate_summary)

    return rows.to_dict('records')


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
