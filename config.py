import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    APP_ID_WHITELIST = os.getenv("APP_ID_WHITELIST").split(",")
    ENVIRONMENT = os.getenv("ENVIRONMENT")