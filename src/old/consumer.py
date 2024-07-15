import logging

import faust

app = faust.App("stock_consumer", broker="kafka://localhost:9092", web_port=6066)
stock_updates_topic = app.topic("stock_updates")  # listen to same topic as in producer
stock_changed_by10_topic = app.topic("stock_chg10")
logger = logging.getLogger("stock_consumer")


@app.agent(stock_updates_topic)
async def process_stock_updates(updates):
    async for update in updates:
        logger.info(f"Consumed: {update}")


@app.agent(stock_changed_by10_topic)
async def process_stock_change(updates):
    async for update in updates:
        logger.info(f"Consumed: {update}")


if __name__ == "__main__":
    app.main()
