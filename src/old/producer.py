# creating a program to simultaneously produce and consume multiple topics.
# ingest events as one Kafka topic and then create new events under a different topic name
# pretend we’re tracking stock-price changes.
import logging
import random

import faust

global prev

STOCK_START = {
    "GOOGL": 20,
    "AAPL": 100,
    "TSLA": 25,
    "MSFT": 22,
    "META": 10,
}

prev = STOCK_START.copy()

app = faust.App("stock_producer", broker="kafka://localhost:9092", web_port=6067)
stock_producer_topic = app.topic("stock_updates")
stock_changed_by10_topic = app.topic("stock_chg10")
logger = logging.getLogger("stock_producer")


def stock_val_change(start_at: int = 40):
    """
    The stocks should have a fixed starting price that you can set up up
    arbitrarily, and the program should either add or subtract values
    randomly from the previous price on a ticker every so often.
    """
    scale = random.randint(1, 10)
    mag = random.choice([-1, 1])
    change = random.random() * scale
    return start_at + (change * mag)


@app.timer(interval=5.0)  # Generate updates every 5 seconds
async def generate_stock_updates():
    prev = STOCK_START.copy()
    for stock, start_at in STOCK_START.items():
        new_value = stock_val_change(start_at)
        logger.info(f"Generated: {stock} updated to {new_value}")
        await stock_producer_topic.send(value={"stock": stock, "value": new_value})


@app.timer(interval=5.0)  # Generate updates every 5 seconds
async def check_stock_change():
    for stock, curr_val in STOCK_START.items():
        prev_val = prev[stock]
        change = (curr_val - prev_val) * 100 / prev_val
        if change > 10:
            logger.info("Change of stock greater than 10%")
        await stock_changed_by10_topic.send(
            value={"stock": stock, "change": change, "caution": change > 10}
        )


if __name__ == "__main__":
    app.main()
