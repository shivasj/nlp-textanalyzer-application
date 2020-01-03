from dataaccess.session import database


if __name__ == "__main__":
    print("Running database setup....")

    cursor = database.cursor()

    # News

    # Articles Table
    sql = """
            CREATE TABLE IF NOT EXISTS articles(
               id TEXT PRIMARY KEY NOT NULL,
               source TEXT NOT NULL,
               article_link TEXT NOT NULL,
               article_date TEXT NOT NULL,
               article_title TEXT NOT NULL,
               article_content TEXT NOT NULL,
               article_dts INTEGER NOT NULL
            );
        """

    print(sql)
    cursor.execute(sql)
