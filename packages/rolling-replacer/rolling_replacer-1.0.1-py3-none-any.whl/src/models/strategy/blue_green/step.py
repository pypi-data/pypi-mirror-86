import logging

from src.utils.aws_autoscaling_group import AutoscalingGroup
from src.utils.aws_load_balancer import LoadBalancer
from src.utils.aws_target_group import TargetGroup


class BlueGreenStep:
    def __init__(
        self,
        step_id: int,
        total_steps: int,
        load_balancer: LoadBalancer,
        autoscaling_group_blue: AutoscalingGroup,
        target_group_blue: TargetGroup,
        autoscaling_group_green: AutoscalingGroup,
        target_group_green: TargetGroup,
    ):
        self.log(f"Step {step_id}/{total_steps}")

        self.load_balancer = load_balancer
        self.autoscaling_group_blue = autoscaling_group_blue
        self.target_group_blue = target_group_blue
        self.autoscaling_group_green = autoscaling_group_green
        self.target_group_green = target_group_green

    def __str__(self) -> str:
        return type(self).__name__

    @property
    def active_target_group(self) -> TargetGroup:
        return (
            self.target_group_green
            if self.load_balancer.arn in self.target_group_green.load_balancers_arns
            else self.target_group_blue
        )

    @property
    def inactive_target_group(self) -> TargetGroup:
        return (
            self.target_group_green
            if self.load_balancer.arn not in self.target_group_green.load_balancers_arns
            else self.target_group_blue
        )

    @property
    def active_autoscaling_group(self) -> AutoscalingGroup:
        return (
            self.autoscaling_group_green
            if self.active_target_group.arn in self.autoscaling_group_green.target_groups_arns
            else self.autoscaling_group_blue
        )

    @property
    def inactive_autoscaling_group(self) -> AutoscalingGroup:
        return (
            self.autoscaling_group_green
            if self.active_target_group.arn not in self.autoscaling_group_green.target_groups_arns
            else self.autoscaling_group_blue
        )

    def log(self, message: str) -> None:
        logging.info(f"[{self}] {message}")

    def execute(self) -> bool:
        return True

    def pre_check(self) -> bool:
        return True

    def post_check(self) -> bool:
        return True
