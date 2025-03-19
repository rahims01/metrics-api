# Metrics API Service

This service provides an API for collecting and exposing metrics from various client applications. It utilizes Apache Kafka for message queuing and Prometheus for metrics monitoring.

## Features

-   **Metrics Collection:** Accepts metrics data from client applications via a REST API endpoint.
-   **Kafka Integration:** Uses Apache Kafka for reliable message queuing between the API and metric consumption.
-   **Prometheus Exporter:** Exposes internal service metrics in Prometheus format for monitoring.
-   **Health Checks:** Provides health status information for service components.
-   **Swagger UI:** Includes a Swagger UI for easy API documentation and testing.

## Directory Structure
Markdown

# Metrics API Service

This service provides an API for collecting and exposing metrics from various client applications. It utilizes Apache Kafka for message queuing and Prometheus for metrics monitoring.

## Features

-   **Metrics Collection:** Accepts metrics data from client applications via a REST API endpoint.
-   **Kafka Integration:** Uses Apache Kafka for reliable message queuing between the API and metric consumption.
-   **Prometheus Exporter:** Exposes internal service metrics in Prometheus format for monitoring.
-   **Health Checks:** Provides health status information for service components.
-   **Swagger UI:** Includes a Swagger UI for easy API documentation and testing.

## Directory Structure

.
├── api
│   ├── init.py
│   └── metrics_handler.py     # Flask blueprint for handling metrics API requests
├── services
│   ├── kafka_consumer.py      # Kafka consumer service
│   └── kafka_producer.py      # Kafka producer service
├── static
│   └── swagger.json           # Swagger API definition
├── templates
│   └── swagger-ui.html        # HTML for Swagger UI
├── app.py                     # Flask application setup
├── config.py                  # Configuration settings
├── main.py                    # Application entry point
├── manifest.yml               # Cloud Foundry deployment manifest
├── .env                       # Environment variables
└── requirements.txt           # Python dependencies

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment Variables:**

    Create a `.env` file in the root directory with the following variables:

    ```
    KAFKA_BOOTSTRAP_SERVERS=localhost:9092  # Kafka broker addresses
    KAFKA_TOPIC=metrics_topic               # Kafka topic for metrics
    APP_ID_WHITELIST=12345                  # Allowed application IDs (comma-separated)
    ENVIRONMENT=development                 # Application environment (development/production)
    ```

3.  **Start Kafka:**

    Ensure you have a Kafka broker running and accessible at the configured `KAFKA_BOOTSTRAP_SERVERS`.

4.  **Run the Application:**

    ```bash
    python main.py
    ```

    The application will start on `http://0.0.0.0:8080`.

## Endpoints

-   `/api/v2/app/{app_id}/metrics` (POST): Submit metrics data.
    -   Requires a JSON payload with an array of metrics.
-   `/api/v2/app/{app_id}/metrics` (GET): Retrieve consumed client metrics.
-   `/api/v2/app/{app_id}/health` (GET): Get service health status.
-   `/prometheus-metrics` (GET): Expose Prometheus metrics.
-   `/`: Swagger UI for API documentation.

## Metrics

The service exposes the following metrics in Prometheus format:

-   `kafka_metrics_sent_total`: Total number of metrics sent to Kafka.
-   `kafka_metrics_sent_created`: Total number of metrics created for sending to Kafka.
-   `kafka_metrics_failed_total`: Total number of metrics failed to send to Kafka.
-   `kafka_metrics_failed_created`: Total number of metrics failed during creation for sending to kafka.
-   `kafka_producer_status`: Kafka producer status (1 for connected, 0 for disconnected).
-   `kafka_consumer_status`: Kafka consumer status (1 for connected, 0 for disconnected).
-   `kafka_metrics_consumed_total`: Total number of metrics consumed from Kafka.
-   `kafka_metrics_consumed_created`: Total number of metrics created after consumption from Kafka.

## Deployment to Cloud Foundry

1.  **Install the Cloud Foundry CLI:**

    Follow the instructions on the Cloud Foundry website to install the CLI.

2.  **Log in to Cloud Foundry:**

    ```bash
    cf login -a <api_endpoint> -u <username> -p <password> -o <org> -s <space>
    ```

3.  **Push the Application:**

    ```bash
    cf push
    ```

    The `manifest.yml` file contains the deployment configuration.

## Using the API

1.  **Submit Metrics:**

    Send a POST request to `/api/v2/app/{app_id}/metrics` with a JSON payload like this:

    ```json
    {
      "metrics": [
        {
          "profileId": "myprofile",
          "timestamp": "2025-03-18T20:00:00.278",
          "payload": {
            "http.server.requests": 1.0
          },
          "tags": {
            "statistic": "count",
            "method": "GET",
            "env": "prod",
            "status": "200"
          }
        }
      ]
    }
    ```

2.  **Retrieve Metrics:**

    Send a GET request to `/api/v2/app/{app_id}/metrics` to retrieve consumed metrics.

3.  **Check Health:**

    Send a GET request to `/api/v2/app/{app_id}/health` to check the service health.

4.  **View Prometheus Metrics:**

    Access `/prometheus-metrics` to view the service metrics in Prometheus format.

5.  **View Swagger UI:**

    Access `/` to view the Swagger UI for API documentation.
