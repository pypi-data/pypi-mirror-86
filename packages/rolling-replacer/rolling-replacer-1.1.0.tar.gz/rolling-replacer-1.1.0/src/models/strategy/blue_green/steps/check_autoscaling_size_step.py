from src.models.strategy.blue_green.step import BlueGreenStep
from src.utils import aws_autoscaling_group


class CheckAutoscalingSizeStep(BlueGreenStep):
    def execute(self) -> bool:
        self.log(
            f'Empty size for inactive autoscaling group: "{self.inactive_autoscaling_group.name}"'
        )

        aws_autoscaling_group.set_size(self.inactive_autoscaling_group.name, 0, 0, 0)

        return True

    def pre_check(self) -> bool:
        self.log(
            f"[PreCheck] active autoscaling property: min_size={self.active_autoscaling_group.min_size}, max_size={self.active_autoscaling_group.max_size}, desired_capacity={self.active_autoscaling_group.desired_capacity}"
        )
        self.log(
            f"[PreCheck] inactive autoscaling property: min_size={self.inactive_autoscaling_group.min_size}, max_size={self.inactive_autoscaling_group.max_size}, desired_capacity={self.inactive_autoscaling_group.desired_capacity}"
        )

        return True

    def post_check(self) -> bool:
        active_autoscaling_group = aws_autoscaling_group.get(self.active_autoscaling_group.name)
        inactive_autoscaling_group = aws_autoscaling_group.get(self.inactive_autoscaling_group.name)

        self.log(
            f"[PostCheck] active autoscaling property: min_size={active_autoscaling_group.min_size}, max_size={active_autoscaling_group.max_size}, desired_capacity={active_autoscaling_group.desired_capacity}"
        )
        self.log(
            f"[PostCheck] inactive autoscaling property: min_size={inactive_autoscaling_group.min_size}, max_size={inactive_autoscaling_group.max_size}, desired_capacity={inactive_autoscaling_group.desired_capacity}"
        )

        return True
