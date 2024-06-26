import faust

app = faust.App(
    "hello-world",
    broker="kafka://localhost:9092",
    value_serializer="raw",  # "raw",
)


greetings_topic = app.topic("greetings")


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(f"Greeting says {greeting}")


if __name__ == "__main__":
    app.main()
