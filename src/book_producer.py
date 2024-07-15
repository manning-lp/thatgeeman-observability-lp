# creating a program to call an api and store the outcome in a database
import logging

import faust
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept": "application/json",
}
API_URL = "https://fakerapi.it/api/v1/books?_quantity=1"  # requests one book
# sample response
"""
{
  "status": "OK",
  "code": 200,
  "total": 1,
  "data": [
    {
      "id": 1,
      "title": "I don't believe.",
      "author": "Destin O'Connell",
      "genre": "Eos",
      "description": "White Rabbit blew three blasts on the door with his knuckles.",
      "isbn": "9783620460652",
      "image": "http://placeimg.com/480/640/any",
      "published": "1986-08-29",
      "publisher": "Illum Blanditiis"
    }
  ]
}
"""


class Books(faust.Record):
    """This is the same as a dataclass"""

    id: int
    title: str
    author: str
    genre: str
    description: str
    isbn: str
    image: str
    published: str
    published: str


app = faust.App("book_producer", broker="kafka://localhost:9092", web_port=6067)
book_producer_topic = app.topic("book_updates", value_type=Books)
logger = logging.getLogger("book_producer")


@app.timer(interval=5.0)  # request the API every 5 seconds
async def generate_book_updates():
    try:
        response = requests.get(url=API_URL, headers=headers)
        data = response.json()["data"][0]
        await book_producer_topic.send(value=data)
        logging.info(f"Produced {data}")
    except Exception as e:
        logging.info(e)


if __name__ == "__main__":
    app.main()
