from typing import List

from src.models.strategy.blue_green.step import BlueGreenStep
from src.utils import aws_instance
from src.utils.aws_autoscaling_group import Instance


class TerminateInactiveInstancesStep(BlueGreenStep):
    @property
    def in_service_instances(self) -> List[Instance]:
        return [
            i for i in self.inactive_autoscaling_group.instances if i.health_status == "InService"
        ]

    def execute(self) -> bool:
        if len(self.in_service_instances) > 0:
            self.log(
                f"Send terminate signal for {','.join(i.id for i in self.in_service_instances)}"
            )
            aws_instance.terminate([i.id for i in self.in_service_instances])

        return True

    def pre_check(self) -> bool:
        if len(self.in_service_instances) == 0:
            self.log(
                f'[PreCheck] No instance to terminate in "{self.inactive_autoscaling_group.name}"'
            )
        else:
            self.log(
                f"[PreCheck] {len(self.in_service_instances)} instance to terminate in \"{self.inactive_autoscaling_group}\": {','.join(i.id for i in self.in_service_instances)}"
            )

        return True

    def post_check(self) -> bool:
        for instance in self.in_service_instances:
            refreshed_instance = aws_instance.get(instance.id)

            self.log(f"[PostCheck] {refreshed_instance.health_status}")

        return True
