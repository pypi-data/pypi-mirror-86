from time import sleep

from src.models.strategy.blue_green.step import BlueGreenStep
from src.utils import aws_autoscaling_group


class WaitUntilNewInstancesAreBootedStep(BlueGreenStep):
    def execute(self) -> bool:
        all_booted = False

        while not all_booted:
            asg = aws_autoscaling_group.get(self.new_autoscaling_group.name)

            all_booted = len(asg.provisioning_instances) == asg.desired_capacity

            if not all_booted:
                self.log(
                    f"Booted instances: {len(asg.provisioning_instances)}. Desired instances: {asg.desired_capacity}. Waiting.."
                )
                sleep(3)

        return True

    def post_check(self) -> bool:
        asg = aws_autoscaling_group.get(self.new_autoscaling_group.name)

        if len(asg.provisioning_instances) == asg.desired_capacity:
            self.log(f"[PostCheck] All instances are booted.")

        return True
