from src.models.strategy.blue_green.step import BlueGreenStep


class WaitUntilInactiveInstancesAreHealthyStep(BlueGreenStep):
    def execute(self) -> bool:
        return True
