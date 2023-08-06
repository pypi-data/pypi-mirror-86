import logging

from src.utils.aws_autoscaling_group import AutoscalingGroup
from src.utils.aws_load_balancer import LoadBalancer, ListenerRule
from src.utils.aws_target_group import TargetGroup


class BlueGreenStep:
    def __init__(
        self,
        step_id: int,
        total_steps: int,
        load_balancer: LoadBalancer,
        autoscaling_group_blue: AutoscalingGroup,
        target_group_blue: TargetGroup,
        listener_rule_blue: ListenerRule,
        autoscaling_group_green: AutoscalingGroup,
        target_group_green: TargetGroup,
        listener_rule_green: ListenerRule,
    ):
        self.log(f"Step {step_id}/{total_steps}")

        self.load_balancer = load_balancer
        self.autoscaling_group_blue = autoscaling_group_blue
        self.target_group_blue = target_group_blue
        self.listener_rule_blue = listener_rule_blue
        self.autoscaling_group_green = autoscaling_group_green
        self.target_group_green = target_group_green
        self.listener_rule_green = listener_rule_green

    def __str__(self) -> str:
        return type(self).__name__

    @property
    def active_target_group(self) -> TargetGroup:
        return self.target_group_green if self.is_green_active else self.target_group_blue

    @property
    def inactive_target_group(self) -> TargetGroup:
        return self.target_group_green if not self.is_green_active else self.target_group_blue

    @property
    def active_autoscaling_group(self) -> AutoscalingGroup:
        return self.autoscaling_group_green if self.is_green_active else self.autoscaling_group_blue

    @property
    def inactive_autoscaling_group(self) -> AutoscalingGroup:
        return (
            self.autoscaling_group_green
            if not self.is_green_active
            else self.autoscaling_group_blue
        )

    @property
    def is_green_active(self) -> bool:
        return int(self.listener_rule_green.priority) < int(self.listener_rule_blue.priority)

    @property
    def new_autoscaling_group(self) -> AutoscalingGroup:
        return self.inactive_autoscaling_group

    @property
    def new_target_group(self) -> TargetGroup:
        return self.inactive_target_group

    @property
    def old_autoscaling_group(self) -> AutoscalingGroup:
        return self.active_autoscaling_group

    @property
    def old_target_group(self) -> TargetGroup:
        return self.active_target_group

    def log(self, message: str) -> None:
        logging.info(f"[{self}] {message}")

    def execute(self) -> bool:
        return True

    def pre_check(self) -> bool:
        return True

    def post_check(self) -> bool:
        return True
