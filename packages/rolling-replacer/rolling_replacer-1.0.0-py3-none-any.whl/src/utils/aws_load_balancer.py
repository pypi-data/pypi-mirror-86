import logging
from dataclasses import dataclass
from typing import List, Optional

import boto3

client = boto3.client("elbv2")
logger = logging.getLogger(__name__)


@dataclass
class LoadBalancer:
    arn: str
    name: str


@dataclass
class TargetGroupStickiness:
    enabled: bool
    seconds: Optional[int]


@dataclass
class WeightedTargetGroup:
    target_group_arn: str
    weight: int


@dataclass
class ForwardConfig:
    target_groups: List[WeightedTargetGroup]
    target_group_stickiness: TargetGroupStickiness


@dataclass
class RedirectConfig:
    host: str
    path: str
    port: str
    protocol: str
    query: str
    status_code: str


@dataclass
class DefaultAction:
    action_type: str
    target_group_arn: Optional[str]
    forward_config: Optional[ForwardConfig]
    redirect_config: Optional[RedirectConfig]


@dataclass
class Listener:
    arn: str
    default_actions: List[DefaultAction]


def get(name: str) -> LoadBalancer:
    logger.debug(f'Get load balancer with name "{name}"')

    response = client.describe_load_balancers(Names=[name])
    logger.debug(response)

    try:
        load_balancer_raw = next(
            lb_raw for lb_raw in response["LoadBalancers"] if lb_raw["LoadBalancerName"] == name
        )

        lb = LoadBalancer(
            arn=load_balancer_raw["LoadBalancerArn"], name=load_balancer_raw["LoadBalancerName"],
        )

        return lb
    except StopIteration:
        logger.error(f'Load balancer "{name}" not found.')
        exit(1)


def get_listeners(load_balancer: LoadBalancer) -> List[Listener]:
    logger.debug(f'Get load balancer listeners with name "{load_balancer.name}"')

    response = client.describe_listeners(LoadBalancerArn=load_balancer.arn)
    logger.debug(response)

    try:
        listeners = []
        listeners_raw = response["Listeners"]

        for listener_raw in listeners_raw:
            arn = listener_raw["ListenerArn"]
            default_actions = []

            for default_action_raw in listener_raw["DefaultActions"]:
                action_type = default_action_raw["Type"]
                target_group_arn = default_action_raw.get("TargetGroupArn")
                forward_config = (
                    ForwardConfig(
                        target_groups=[
                            WeightedTargetGroup(
                                target_group_arn=weighted_target_group_raw["TargetGroupArn"],
                                weight=weighted_target_group_raw["Weight"],
                            )
                            for weighted_target_group_raw in default_action_raw["ForwardConfig"][
                                "TargetGroups"
                            ]
                        ],
                        target_group_stickiness=TargetGroupStickiness(
                            enabled=default_action_raw["ForwardConfig"][
                                "TargetGroupStickinessConfig"
                            ]["Enabled"],
                            seconds=default_action_raw["ForwardConfig"][
                                "TargetGroupStickinessConfig"
                            ].get("Seconds"),
                        ),
                    )
                    if action_type == "forward"
                    else None
                )
                redirect_config = (
                    RedirectConfig(
                        host=default_action_raw.get("RedirectConfig", {}).get("Host"),
                        path=default_action_raw.get("RedirectConfig", {}).get("Path"),
                        port=default_action_raw.get("RedirectConfig", {}).get("Port"),
                        protocol=default_action_raw.get("RedirectConfig", {}).get("Protocol"),
                        query=default_action_raw.get("RedirectConfig", {}).get("Query"),
                        status_code=default_action_raw.get("RedirectConfig", {}).get("StatusCode"),
                    )
                    if action_type == "redirect"
                    else None
                )

                default_actions.append(
                    DefaultAction(
                        action_type=action_type,
                        target_group_arn=target_group_arn,
                        forward_config=forward_config,
                        redirect_config=redirect_config,
                    )
                )

            listeners.append(Listener(arn=arn, default_actions=default_actions))

        return listeners
    except StopIteration:
        logger.error(f'Load balancer "{load_balancer.name}" not found.')
        exit(1)


def set_target_group(load_balancer: LoadBalancer, target_group_arn: str) -> bool:
    listeners = get_listeners(load_balancer)

    listener_arn = next(
        listener.arn
        for listener in listeners
        if any(
            default_action.action_type == "forward" for default_action in listener.default_actions
        )
    )

    client.modify_listener(
        ListenerArn=listener_arn,
        DefaultActions=[
            {
                "Type": "forward",
                "ForwardConfig": {
                    "TargetGroups": [{"TargetGroupArn": target_group_arn, "Weight": 1},],
                },
            }
        ],
    )

    return True
