import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from typing import Any, Dict, List

from dataaccess.session import database


async def browse_by_entity(entity:str,
                           day: int = 0,
                           hours: int = None,top:int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve a list of rows from the database
    """

    today = datetime.today()
    end_time = datetime(today.year, today.month, today.day, 0, 0) - timedelta(days=day)
    start_time = end_time - timedelta(hours=hours)

    sql = """
    select name,entity,count(*)  as count
    from named_entities  
    where entity='{0}' 
    and day_dts >= {1}  and day_dts <= {2}
    group by name,entity 
    order by count(*) desc
    limit {3}
    """

    sql = sql.format(entity,start_time.timestamp(),end_time.timestamp(),top)

    print(sql)
    rows = pd.read_sql_query(sql, database)

    return rows.to_dict('records')
