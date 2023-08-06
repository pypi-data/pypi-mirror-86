from src.models.strategy.blue_green.step import BlueGreenStep


class CheckActiveStep(BlueGreenStep):
    def execute(self) -> bool:
        self.log(f'active autoscaling="{self.active_autoscaling_group.name}"')
        self.log(f'active target group="{self.active_target_group.name}"')
        self.log(f'inactive autoscaling="{self.inactive_autoscaling_group.name}"')
        self.log(f'inactive target group="{self.inactive_target_group.name}"')

        return True
