import logging

import faust
import psycopg

from .book_producer import Books

app = faust.App("book_consumer", broker="kafka://localhost:9092", web_port=6066)
book_updates_topic = app.topic(
    "book_updates", value_type=Books
)  # listen to same topic as in producer
logger = logging.getLogger("book_consumer")


connection_parameters = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "",
    "host": "localhost",  # defaults to localhost if not provided
    "port": "5432",  # defaults to 5432 if not provided
}

# create table first to store into db
# it can also be simply a variable with the command
try:
    with psycopg.connect(**connection_parameters) as conn:
        with conn.cursor() as cur:
            cur.execute(open("../gen_books", "r").read())
except (psycopg.DatabaseError, Exception) as error:
    logging.info(error)


@app.agent(book_updates_topic)
async def process_stock_updates(books):
    async for book in books:
        logging.info(f"Got {book}")
        connection = psycopg.connect(**connection_parameters)
        try:
            with connection as conn:
                with conn.cursor() as cur:
                    sql = """INSERT INTO gen_books(book_isbn, title, author, published) VALUES(%s, %s, %s, %s);"""
                    cur.execute(
                        sql, (book.isbn, book.title, book.author, book.published)
                    )
                    # Make the changes to the database persistent
                conn.commit()
        except (psycopg.DatabaseError, Exception) as error:
            logging.info(error)
        logging.info(f"Wrote {book.isbn} to database")


if __name__ == "__main__":
    app.main()
