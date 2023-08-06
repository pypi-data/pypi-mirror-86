from time import sleep

from src.models.strategy.blue_green.step import BlueGreenStep
from src.utils import aws_autoscaling_group, aws_target_group


class WaitUntilNewInstancesAreTargetedStep(BlueGreenStep):
    def execute(self) -> bool:
        all_targeted = False

        asg = aws_autoscaling_group.get(self.new_autoscaling_group.name)

        while not all_targeted:
            tg = aws_target_group.get(self.new_target_group.name)

            pending_targets = [
                target for target in tg.provisioning_targets if target.status != "healthy"
            ]
            all_targeted = len(pending_targets) == 0

            if not all_targeted:
                self.log(
                    f"Pending target instances: {len(pending_targets)}. All instances: {asg.desired_capacity}. Waiting.."
                )
                sleep(3)

        self.log(f"{len(asg.instances)} total instances to replace.")

        return True

    def post_check(self) -> bool:
        asg = aws_autoscaling_group.get(self.new_autoscaling_group.name)
        tg = aws_target_group.get(self.new_target_group.name)

        if (
            asg.desired_capacity
            == len(asg.instances)
            == len([target for target in tg.targets if target.status == "healthy"])
        ):
            self.log(f"[PostCheck] All instances are healthy")
        return True
