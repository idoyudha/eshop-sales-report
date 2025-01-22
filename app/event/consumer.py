import json
import logging
import asyncio

from typing import Dict, Any
from uuid import UUID

from confluent_kafka import Consumer, KafkaError, KafkaException

from app.core.config import settings
from app.core.db import async_session_factory
from app.models.kafka_sale import KafkaSaleCreated
from app.service.sale import create_sale_service

logger = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVER,
            'group.id': settings.KAFKA_CONSUMER_GROUP,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        })
        self.running = True

    def _deserialize_message(self, message: bytes) -> Dict[str, Any]:
        try:
            data = json.loads(message.decode('utf-8'))
            # Convert string UUIDs to UUID objects
            for key in ['product_id', 'user_id', 'order_id']:
                if key in data and isinstance(data[key], str):
                    data[key] = UUID(data[key])
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message: {e}")
            raise
        except ValueError as e:
            logger.error(f"Failed to parse UUID: {e}")
            raise

    async def process_message(self, message: Dict[str, Any]) -> None:
        # create a new session for each message
        async with async_session_factory() as session:
            try:
                sale_created_data = KafkaSaleCreated.model_validate(message)
                sales = await create_sale_service(session=session, input=sale_created_data)
                await session.commit()
                logger.info(f"Processed sale with order IDs: {[sale.order_id for sale in sales]}")
            except Exception as e:
                logger.error(f"Failed to process message: {e}")
                await session.rollback()
                raise

    async def start(self):
        try:
            self.consumer.subscribe([settings.KAFKA_TOPIC_SALE_CREATED])
            logger.info(f"Subscribed to topic: {settings.KAFKA_TOPIC_SALE_CREATED}")

            while self.running:
                try:
                    # poll messages with timeout
                    msg = self.consumer.poll(timeout=1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            logger.debug('Reached end of partition')
                        else:
                            logger.error(f'Error while consuming message: {msg.error()}')
                        continue
                    
                    # process message
                    try:
                        value = self._deserialize_message(msg.value())
                        await self.process_message(value)
                        self.consumer.commit(msg)
                    except Exception as e:
                        logger.error(f"Failed to process message: {e}")
                        continue

                except KafkaException as e:
                    logger.error(f"Kafka error: {e}")
                    continue
                
                # add small delay to prevent CPU overuse
                await asyncio.sleep(0.1)
        
        except Exception as e:
            logger.error(f"Fatal error in consumer: {e}")
            raise
        finally:
            # close down consumer to commit final offsets.
            self.consumer.close()
            logger.info("Kafka consumer closed")