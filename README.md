# observability-lp-author
Repository for liveProject: Kafka: Observability

# faust

1. Install faust-streaming (community edition of faust)
2. Run `docker compose up -d`
3. To consume messages from a topic called `greetings` (full history):
   1. `docker compose exec -it kafka  /opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic greetings --from-beginning`
   2. This executes the consumer 
   3. Alternatively, On a different terminal run `python src/faust_app.py worker -l info` to run the consumer
      1. This terminal will show the consumer logs, but only since program start (limited history).
4. Now send messages from the `faust_app.py` script and showing up in the consumer window!
   1. Execute `faust -A faust_app send @greet "Hello Faust"` based on the [guide](https://faust-streaming.github.io/faust/playbooks/quickstart.html)
   2. This part is the creator. 
