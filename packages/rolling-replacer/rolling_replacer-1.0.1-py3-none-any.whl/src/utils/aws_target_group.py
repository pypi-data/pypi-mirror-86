import logging
from dataclasses import dataclass
from typing import List

import boto3

client = boto3.client("elbv2")
logger = logging.getLogger(__name__)


@dataclass
class TargetGroup:
    arn: str
    name: str
    load_balancers_arns: List[str]


def get(name: str) -> TargetGroup:
    logger.debug(f'Get target group with name "{name}"')

    response = client.describe_target_groups(Names=[name])
    logger.debug(response)

    try:
        target_group_raw = next(
            tg_raw for tg_raw in response["TargetGroups"] if tg_raw["TargetGroupName"] == name
        )

        return TargetGroup(
            arn=target_group_raw["TargetGroupArn"],
            name=target_group_raw["TargetGroupName"],
            load_balancers_arns=target_group_raw["LoadBalancerArns"],
        )
    except StopIteration:
        logger.error(f'Target group "{name}" not found.')
        exit(1)
