import logging
from dataclasses import dataclass
from typing import List, Optional, Dict

import boto3

client = boto3.client("elbv2")
logger = logging.getLogger(__name__)


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
class Action:
    action_type: str
    target_group_arn: Optional[str]
    forward_config: Optional[ForwardConfig]
    redirect_config: Optional[RedirectConfig]


@dataclass
class ListenerRule:
    arn: str
    priority: int
    is_default: bool
    actions: List[Action]


@dataclass
class Listener:
    arn: str
    rules: List[ListenerRule]


@dataclass
class LoadBalancer:
    arn: str
    name: str
    listeners: List[Listener]


def get(name: str) -> LoadBalancer:
    logger.debug(f'Get load balancer with name "{name}"')

    response = client.describe_load_balancers(Names=[name])
    logger.debug(response)

    try:
        load_balancer_raw = next(
            lb_raw for lb_raw in response["LoadBalancers"] if lb_raw["LoadBalancerName"] == name
        )

        lb = LoadBalancer(
            arn=load_balancer_raw["LoadBalancerArn"],
            name=load_balancer_raw["LoadBalancerName"],
            listeners=get_listeners(load_balancer_raw["LoadBalancerArn"]),
        )

        return lb
    except StopIteration:
        logger.error(f'Load balancer "{name}" not found.')
        exit(1)


def get_listeners(load_balancer_arn: str) -> List[Listener]:
    logger.debug(f'Get load balancer listeners with name "{load_balancer_arn}"')

    response = client.describe_listeners(LoadBalancerArn=load_balancer_arn)
    logger.debug(response)

    try:
        listeners = []
        listeners_raw = response["Listeners"]

        for listener_raw in listeners_raw:
            arn = listener_raw["ListenerArn"]

            listeners.append(Listener(arn=arn, rules=get_listener_rules(arn)))

        return listeners
    except StopIteration:
        logger.error(f'Load balancer "{load_balancer_arn}" not found.')
        exit(1)


def get_listener_rules(listener_arn: str) -> List[ListenerRule]:
    logger.debug(f'Get rule listener with arn "{listener_arn}"')

    response = client.describe_rules(ListenerArn=listener_arn)
    logger.debug(response)

    try:
        rules = []
        rules_raw = response["Rules"]

        for rule_raw in rules_raw:
            rules.append(
                ListenerRule(
                    arn=rule_raw["RuleArn"],
                    priority=int(rule_raw["Priority"]) if rule_raw["Priority"] != "default" else 0,
                    actions=[__parse_rule_action(action_raw) for action_raw in rule_raw["Actions"]],
                    is_default=rule_raw["IsDefault"],
                )
            )

        return rules
    except StopIteration:
        logger.error(f'Listener with arn "{listener_arn}" not found.')
        exit(1)


def get_listener_rule(listener_rule_arn: str) -> ListenerRule:
    logger.debug(f'Get rule with arn "{listener_rule_arn}"')

    response = client.describe_rules(RuleArns=[listener_rule_arn])
    logger.debug(response)

    try:
        listener_rule_raw = next(
            rule_raw for rule_raw in response["Rules"] if rule_raw["RuleArn"] == listener_rule_arn
        )

        return ListenerRule(
            arn=listener_rule_raw["RuleArn"],
            priority=int(listener_rule_raw["Priority"])
            if listener_rule_raw["Priority"] != "default"
            else 0,
            actions=[
                __parse_rule_action(action_raw) for action_raw in listener_rule_raw["Actions"]
            ],
            is_default=listener_rule_raw["IsDefault"],
        )
    except StopIteration:
        logger.error(f'Rule with arn "{listener_rule_arn}" not found.')
        exit(1)


def __parse_rule_action(raw: Dict) -> Action:
    action_type = raw["Type"]
    target_group_arn = raw.get("TargetGroupArn")
    forward_config = (
        ForwardConfig(
            target_groups=[
                WeightedTargetGroup(
                    target_group_arn=weighted_target_group_raw["TargetGroupArn"],
                    weight=weighted_target_group_raw["Weight"],
                )
                for weighted_target_group_raw in raw["ForwardConfig"]["TargetGroups"]
            ],
            target_group_stickiness=TargetGroupStickiness(
                enabled=raw["ForwardConfig"]["TargetGroupStickinessConfig"]["Enabled"],
                seconds=raw["ForwardConfig"]["TargetGroupStickinessConfig"].get("Seconds"),
            ),
        )
        if action_type == "forward"
        else None
    )
    redirect_config = (
        RedirectConfig(
            host=raw.get("RedirectConfig", {}).get("Host"),
            path=raw.get("RedirectConfig", {}).get("Path"),
            port=raw.get("RedirectConfig", {}).get("Port"),
            protocol=raw.get("RedirectConfig", {}).get("Protocol"),
            query=raw.get("RedirectConfig", {}).get("Query"),
            status_code=raw.get("RedirectConfig", {}).get("StatusCode"),
        )
        if action_type == "redirect"
        else None
    )

    return Action(
        action_type=action_type,
        target_group_arn=target_group_arn,
        redirect_config=redirect_config,
        forward_config=forward_config,
    )


def set_rules_priority(
    listener_rule_arn_1: str,
    listener_rule_priority_1: int,
    listener_rule_arn_2: str,
    listener_rule_priority_2: int,
) -> bool:
    response = client.set_rule_priorities(
        RulePriorities=[
            {"Priority": listener_rule_priority_1, "RuleArn": listener_rule_arn_1},
            {"Priority": listener_rule_priority_2, "RuleArn": listener_rule_arn_2},
        ],
    )
    logger.debug(response)

    return True
