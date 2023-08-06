import boto3

from src.models.strategy.blue_green.step import BlueGreenStep
from src.utils import aws_load_balancer

client = boto3.client("elbv2")


class ReRouteTrafficStep(BlueGreenStep):
    def execute(self) -> bool:
        aws_load_balancer.set_rules_priority(
            self.listener_rule_blue.arn,
            self.listener_rule_green.priority,
            self.listener_rule_green.arn,
            self.listener_rule_blue.priority,
        )

        return True
