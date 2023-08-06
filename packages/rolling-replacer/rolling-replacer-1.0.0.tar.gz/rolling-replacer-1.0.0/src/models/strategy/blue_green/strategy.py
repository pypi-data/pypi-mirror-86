import logging

from src.models.strategy.blue_green.steps.check_active_step import CheckActiveStep
from src.models.strategy.blue_green.steps.check_autoscaling_size_step import (
    CheckAutoscalingSizeStep,
)
from src.models.strategy.blue_green.steps.rereoute_traffic_step import ReRouteTrafficStep
from src.models.strategy.blue_green.steps.set_new_autoscaling_group_size import (
    SetNewAutoscalingGroupSizeStep,
)
from src.models.strategy.blue_green.steps.set_old_autoscaling_group_size import (
    SetOldAutoscalingGroupSizeStep,
)
from src.models.strategy.blue_green.steps.terminate_inactive_instances_step import (
    TerminateInactiveInstancesStep,
)
from src.models.strategy.stategy import Strategy
from src.utils import aws_load_balancer, aws_autoscaling_group, aws_target_group
from src.utils.aws_autoscaling_group import AutoscalingGroup
from src.utils.aws_load_balancer import LoadBalancer
from src.utils.aws_target_group import TargetGroup

logger = logging.getLogger(__name__)


class BlueGreenStrategy(Strategy):
    _load_balancer: LoadBalancer = None
    _autoscaling_group_blue: AutoscalingGroup = None
    _target_group_blue: TargetGroup = None
    _autoscaling_group_green: AutoscalingGroup = None
    _target_group_green: TargetGroup = None

    steps = [
        CheckActiveStep,
        CheckAutoscalingSizeStep,
        TerminateInactiveInstancesStep,
        SetNewAutoscalingGroupSizeStep,
        ReRouteTrafficStep,
        SetOldAutoscalingGroupSizeStep,
    ]

    def __init__(
        self,
        load_balancer_name: str,
        autoscaling_group_blue_name: str,
        target_group_blue_name: str,
        autoscaling_group_green_name: str,
        target_group_green_name: str,
    ):
        self.load_balancer_name = load_balancer_name
        self.autoscaling_group_blue_name = autoscaling_group_blue_name
        self.target_group_blue_name = target_group_blue_name
        self.autoscaling_group_green_name = autoscaling_group_green_name
        self.target_group_green_name = target_group_green_name

    @property
    def load_balancer(self) -> LoadBalancer:
        if self._load_balancer is None:
            self._load_balancer = aws_load_balancer.get(self.load_balancer_name)

        return self._load_balancer

    @property
    def autoscaling_group_blue(self) -> AutoscalingGroup:
        if self._autoscaling_group_blue is None:
            self._autoscaling_group_blue = aws_autoscaling_group.get(
                self.autoscaling_group_blue_name
            )

        return self._autoscaling_group_blue

    @property
    def autoscaling_group_green(self) -> AutoscalingGroup:
        if self._autoscaling_group_green is None:
            self._autoscaling_group_green = aws_autoscaling_group.get(
                self.autoscaling_group_green_name
            )

        return self._autoscaling_group_green

    @property
    def target_group_blue(self) -> TargetGroup:
        if self._target_group_blue is None:
            self._target_group_blue = aws_target_group.get(self.target_group_blue_name)

        return self._target_group_blue

    @property
    def target_group_green(self) -> TargetGroup:
        if self._target_group_green is None:
            self._target_group_green = aws_target_group.get(self.target_group_green_name)

        return self._target_group_green

    def execute(self) -> bool:
        for idx, step_class in enumerate(self.steps):
            step = step_class(
                idx + 1,
                len(self.steps),
                self.load_balancer,
                self.autoscaling_group_blue,
                self.target_group_blue,
                self.autoscaling_group_green,
                self.target_group_green,
            )

            step.pre_check()
            step.execute()
            step.post_check()

        return True
