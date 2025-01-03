from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "eshop-sales-report"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ## Kafka
    KAFKA_BOOTSTRAP_SERVERS: List[str]
    KAFKA_TOPIC_SALE_CREATED: str = "sale-created"
    KAFKA_CONSUMER_GROUP: str = "sale-group"

    class Config:
        env_file = ".env"

settings = Settings()