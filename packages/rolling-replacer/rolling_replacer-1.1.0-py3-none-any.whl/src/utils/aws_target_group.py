import logging
from dataclasses import dataclass
from typing import List

import boto3

client = boto3.client("elbv2")
logger = logging.getLogger(__name__)


@dataclass
class Target:
    id: str
    status: str


@dataclass
class TargetGroup:
    arn: str
    load_balancers_arns: List[str]
    name: str
    targets: List[Target]


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
            load_balancers_arns=target_group_raw["LoadBalancerArns"],
            name=target_group_raw["TargetGroupName"],
            targets=get_targets(target_group_raw["TargetGroupArn"]),
        )
    except StopIteration:
        logger.error(f'Target group "{name}" not found.')
        exit(1)


def get_targets(arn: str) -> List[Target]:
    logger.debug(f'Get targets health with arn "{arn}"')

    response = client.describe_target_health(TargetGroupArn=arn)
    logger.debug(response)

    try:
        return [
            Target(id=tg_raw["Target"]["Id"], status=tg_raw["TargetHealth"]["State"])
            for tg_raw in response["TargetHealthDescriptions"]
        ]
    except StopIteration:
        logger.error(f'Target with arn "{arn}" not found.')
        exit(1)
