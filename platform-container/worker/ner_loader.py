import pandas as pd
from datetime import datetime
import asyncio

import en_core_web_sm
nlp = en_core_web_sm.load()

from dataaccess import data_utils
from dataaccess import articles

def run():
    # Clear existing data for all models
    data_utils.drop_table("named_entities")

    # Generate NER
    loop = asyncio.get_event_loop()
    articles_list = loop.run_until_complete(articles.browse(hours=120))
    ner_list = []
    for article in articles_list:
        # Merge title with content
        text = article['article_title'] + ". " + article["article_content"]
        doc = nlp(text)
        article_date = datetime.fromtimestamp(article['article_dts'])
        for ne in doc.ents:
            ner_list.append({
                'source':article['source'],
                'name':ne.text,
                'entity':ne.label_,
                'day_dts':datetime(article_date.year, article_date.month, article_date.day,0 ,0).timestamp()
            })

    ner_df = pd.DataFrame(ner_list)

    # Save the results
    data_utils.load_data_from_df(ner_df, "named_entities", if_exists='append')

if __name__ == "__main__":
    run()
