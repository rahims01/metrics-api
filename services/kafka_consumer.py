from confluent_kafka import Consumer, KafkaError
from config import Config
import json
from prometheus_client import Gauge, Counter

kafka_consumer_status = Gauge('kafka_consumer_status', 'Kafka consumer status, 1 for connected, 0 for disconnected')
kafka_metrics_consumed_total = Counter('kafka_metrics_consumed_total', 'Total number of metrics consumed from Kafka')
kafka_metrics_consumed_created = Counter('kafka_metrics_consumed_created', 'Total number of metrics created after consumption from Kafka')

class KafkaConsumerService:
    def __init__(self):
        self.consumer = None
        self.connect()
        self.consumed_metrics = []

    def connect(self):
        try:
            self.consumer = Consumer({
                'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS,
                'group.id': 'metrics-consumer-group',
                'auto.offset.reset': 'earliest'
            })
            self.consumer.subscribe([Config.KAFKA_TOPIC])
            kafka_consumer_status.set(1)
        except Exception as e:
            print(f"Error connecting to Kafka: {e}")
            kafka_consumer_status.set(0)

    def consume(self):
        if not self.consumer:
            self.connect()
            if not self.consumer:
                return []

        messages = []
        try:
            msg = self.consumer.poll(1.0)
            if msg is None:
                return []
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    return []
                else:
                    print(f"Consumer error: {msg.error()}")
                    return []

            message_value = json.loads(msg.value().decode('utf-8'))
            messages.append(message_value)
            kafka_metrics_consumed_total.inc()
            kafka_metrics_consumed_created.inc()
        except Exception as e:
            print(f"Consumer poll error: {e}")
        return messages

    def get_consumed_metrics(self):
        return self.consumed_metrics