import logging
from dataclasses import dataclass
from typing import List

import boto3

client = boto3.resource("ec2")
logger = logging.getLogger(__name__)


@dataclass
class Instance:
    health_status: str
    id: str
    lifecycle_state: str


def get(identifier: str) -> Instance:
    logger.debug(f'Get instance with id "{id}"')

    response = client.instances.filter(InstanceIds=[identifier])
    logger.debug(response)

    try:
        instance_raw = next(
            i_raw for i_raw in response["Instances"] if i_raw["LoadBalancerName"] == identifier
        )

        return Instance(
            id=instance_raw["InstanceId"],
            health_status=instance_raw["HealthStatus"],
            lifecycle_state=instance_raw["LifecycleState"],
        )
    except StopIteration:
        logger.error(f'Instance "{identifier}" not found.')
        exit(1)


def terminate(identifiers: List[str]) -> bool:
    logging.debug(f"Terminate instance {','.join(identifiers)}")

    client.instances.filter(InstanceIds=[identifiers]).terminate()

    return True
