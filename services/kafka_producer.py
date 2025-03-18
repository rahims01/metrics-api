from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from config import Config
import json
from prometheus_client import Gauge, Counter

kafka_metrics_sent_total = Counter('kafka_metrics_sent_total', 'Total number of metrics sent to Kafka')
kafka_metrics_sent_created = Counter('kafka_metrics_sent_created', 'Total number of metrics created for sending to Kafka')
kafka_metrics_failed_total = Counter('kafka_metrics_failed_total', 'Total number of metrics failed to send to Kafka')
kafka_metrics_failed_created = Counter('kafka_metrics_failed_created', 'Total number of metrics failed during creation for sending to kafka')
kafka_producer_status = Gauge('kafka_producer_status', 'Kafka producer status, 1 for connected, 0 for disconnected')


def create_topic():
    admin_client = AdminClient({'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS})
    topic_list = [NewTopic(Config.KAFKA_TOPIC, num_partitions=1, replication_factor=1)]
    try:
        admin_client.create_topics(topic_list)
    except Exception as e:
        print(f"Topic creation failed: {e}")


class KafkaProducerService:
    def __init__(self):
        self.producer = None
        self.connect()
        create_topic()

    def connect(self):
        try:
            self.producer = Producer({
                'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS
            })
            kafka_producer_status.set(1)
        except Exception as e:
            print(f"Error connecting to Kafka: {e}")
            kafka_producer_status.set(0)

    def produce(self, message):
        if not self.producer:
            self.connect()
            if not self.producer:
                kafka_metrics_failed_total.inc()
                return False

        try:
            kafka_metrics_sent_created.inc()
            self.producer.produce(Config.KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
            self.producer.flush()
            kafka_metrics_sent_total.inc()
            return True
        except Exception as e:
            print(f"Error producing message: {e}")
            kafka_metrics_failed_total.inc()
            return False