import logging
from dataclasses import dataclass
from typing import List, Optional

import boto3

from src.utils.aws_instance import Instance

client = boto3.client("autoscaling")
logger = logging.getLogger(__name__)


@dataclass
class AutoscalingGroup:
    arn: str
    desired_capacity: int
    instances: List[Instance]
    max_size: int
    min_size: int
    name: str
    target_groups_arns: List[str]


def get(name: str) -> AutoscalingGroup:
    logger.debug(f'Get autoscaling group with name "{name}"')

    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[name])
    logger.debug(response)

    try:
        autoscaling_group_raw = next(
            asg_raw
            for asg_raw in response["AutoScalingGroups"]
            if asg_raw["AutoScalingGroupName"] == name
        )

        return AutoscalingGroup(
            arn=autoscaling_group_raw["AutoScalingGroupARN"],
            name=autoscaling_group_raw["AutoScalingGroupName"],
            min_size=autoscaling_group_raw["MinSize"],
            max_size=autoscaling_group_raw["MaxSize"],
            desired_capacity=autoscaling_group_raw["DesiredCapacity"],
            instances=[
                Instance(
                    id=instance["InstanceId"],
                    health_status=instance["HealthStatus"],
                    lifecycle_state=instance["LifecycleState"],
                )
                for instance in autoscaling_group_raw["Instances"]
            ],
            target_groups_arns=autoscaling_group_raw["TargetGroupARNs"],
        )
    except StopIteration:
        logger.error(f'Autoscaling group "{name}" not found.')
        exit(1)


def set_size(
    name: str,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    desired_capacity: Optional[int] = None,
) -> bool:
    args = dict()

    if min_size is not None:
        args["MinSize"] = min_size

    if max_size is not None:
        args["MaxSize"] = max_size

    if desired_capacity is not None:
        args["DesiredCapacity"] = desired_capacity

    client.update_auto_scaling_group(AutoScalingGroupName=name, **args)

    return True
