import os
from typing import Any, Callable, Dict, Optional, Union

from kafka import KafkaConsumer, KafkaProducer


def create_producer(
    prefix: str,
    value_serializer: Optional[Callable[[Any], bytes]] = None,
    client_id: Optional[str] = None,
    acks: Union[int, str] = 1,
) -> KafkaProducer:
    """Create Kafka producer

    Creates kafka producer based on prefixed env vars.

    Supported variables:
    - PREFIX_BOOTSTRAP_SERVERS (also PREFIX_BOOTSTRAP_SERVERS)
    - PREFIX_SECURITY_PROTOCOL (defaults to "PLAINTEXT")
    - PREFIX_SASL_MECHANISM
    - PREFIX_SASL_USERNAME
    - PREFIX_SASL_PASSWORD

    Args:
        prefix: prefix for env vars
        value_serializer: Function used for turning objects into bytes
        client_id: Descriptive name. (Default: kafka-python-{version})
        acks: 0, 1 or 'all'

    """
    try:
        bootstrap_servers = os.environ[f"{prefix}_BOOTSTRAP_SERVERS"].split(",")
    except KeyError:
        bootstrap_servers = os.environ[f"{prefix}_BOOTSTRAP_SERVER"].split(",")
    security_protocol = os.environ.get(f"{prefix}_SECURITY_PROTOCOL", "PLAINTEXT")
    kafka_kwargs: Dict[str, Any] = dict(security_protocol=security_protocol)
    if security_protocol == "SASL_PLAINTEXT":
        kafka_kwargs["sasl_mechanism"] = os.environ[f"{prefix}_SASL_MECHANISM"]
        kafka_kwargs["sasl_plain_username"] = os.environ[f"{prefix}_SASL_USERNAME"]
        kafka_kwargs["sasl_plain_password"] = os.environ[f"{prefix}_SASL_PASSWORD"]
    if value_serializer:
        kafka_kwargs["value_serializer"] = value_serializer
    if client_id:
        kafka_kwargs["client_id"] = client_id

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers, acks=acks, **kafka_kwargs
    )
    return producer


def create_consumer(
    prefix: str,
    value_deserializer: Callable[[bytes], Any] = None,
    client_id: Optional[str] = None,
) -> KafkaConsumer:
    """Create Kafka consumer

    Creates kafka consumer based on prefixed env vars.

    Supported variables:
    - PREFIX_BOOTSTRAP_SERVERS (also PREFIX_BOOTSTRAP_SERVERS)
    - PREFIX_CONSUMER_GROUP
    - PREFIX_SECURITY_PROTOCOL (defaults to "PLAINTEXT")
    - PREFIX_SASL_MECHANISM
    - PREFIX_SASL_USERNAME
    - PREFIX_SASL_PASSWORD

    Args:
        prefix: prefix for env vars
        value_deserializer: Function used for turning bytes into objects
        client_id: Descriptive name. (Default: kafka-python-{version})
    """
    try:
        bootstrap_servers = os.environ[f"{prefix}_BOOTSTRAP_SERVERS"].split(",")
    except KeyError:
        bootstrap_servers = os.environ[f"{prefix}_BOOTSTRAP_SERVER"].split(",")
    security_protocol = os.environ.get(f"{prefix}_SECURITY_PROTOCOL", "PLAINTEXT")
    kafka_kwargs: Dict[str, Any] = dict(security_protocol=security_protocol)
    if security_protocol == "SASL_PLAINTEXT":
        kafka_kwargs["sasl_mechanism"] = os.environ[f"{prefix}_SASL_MECHANISM"]
        kafka_kwargs["sasl_plain_username"] = os.environ[f"{prefix}_SASL_USERNAME"]
        kafka_kwargs["sasl_plain_password"] = os.environ[f"{prefix}_SASL_PASSWORD"]
    if value_deserializer:
        kafka_kwargs["value_deserializer"] = value_deserializer
    if client_id:
        kafka_kwargs["client_id"] = client_id
    group_id = os.environ.get(f"{prefix}_CONSUMER_GROUP")
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers, group_id=group_id, **kafka_kwargs
    )
    return consumer
