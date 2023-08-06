import boto3

from src.models.strategy.blue_green.step import BlueGreenStep
from src.utils import aws_load_balancer

client = boto3.client("elbv2")


class ReRouteTrafficStep(BlueGreenStep):
    def execute(self) -> bool:
        aws_load_balancer.set_target_group(self.load_balancer, self.inactive_target_group.arn)

        return True
