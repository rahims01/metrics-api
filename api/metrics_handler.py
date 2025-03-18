from flask import Blueprint, request, jsonify
from services.kafka_producer import KafkaProducerService
from services.kafka_consumer import KafkaConsumerService
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge, Summary, Histogram
import config
import json

metrics_bp = Blueprint('metrics', __name__)

producer = KafkaProducerService(config.KAFKA_BOOTSTRAP_SERVERS, config.KAFKA_TOPIC)
consumer = KafkaConsumerService(config.KAFKA_BOOTSTRAP_SERVERS, config.KAFKA_TOPIC)

metrics_received_total = Counter('metrics_received_total', 'Total number of metrics received')
metrics_forwarded_total = Counter('metrics_forwarded_total', 'Total number of metrics forwarded to Kafka')
metrics_retrieved_total = Counter('metrics_retrieved_total', 'Total number of metrics retrieved')

@metrics_bp.route('/v2/app/<app_id>/metrics', methods=['POST'])
def submit_metrics(app_id):
    if app_id != config.APP_ID:
        return jsonify({"message": "Invalid app ID"}), 401

    try:
        data = request.get_json()
        metrics_received_total.inc()
        producer.produce(data)
        metrics_forwarded_total.inc()
        return jsonify({"message": "Metrics accepted"}), 202
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

@metrics_bp.route('/v2/app/<app_id>/metrics', methods=['GET'])
def get_metrics(app_id):
    if app_id != config.APP_ID:
        return jsonify({"message": "Invalid app ID"}), 401
    try:
        metrics = consumer.get_consumed_metrics()
        metrics_retrieved_total.inc()
        return jsonify({"metrics": metrics, "total_count": len(metrics), "consumer_status": "connected" if consumer.consumer else "disconnected"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

@metrics_bp.route('/prometheus-metrics', methods=['GET'])
def prometheus_metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@metrics_bp.route('/v2/app/<app_id>/health', methods=['GET'])
def health_check(app_id):
    if app_id != config.APP_ID:
        return jsonify({"message": "Invalid app ID"}), 401
    try:
        health_response = {
            "status": "healthy",
            "components": {
                "kafka_producer": {
                    "status": "connected" if producer.producer else "disconnected",
                    "details": "Kafka producer status"
                },
                "kafka_consumer": {
                    "status": "connected" if consumer.consumer else "disconnected",
                    "details": "Consumer status"
                },
                "metrics_stats": {
                    "total_received": producer.kafka_metrics_sent_created._value.get(),
                    "successfully_sent": producer.kafka_metrics_sent_total._value.get(),
                    "failed_sends": producer.kafka_metrics_failed_total._value.get()
                }
            },
            "environment": Config.ENVIRONMENT,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200 \
 \
            @ metrics_bp.route('/prometheus-metrics', methods=['GET'])

        def prometheus_metrics():
            return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}