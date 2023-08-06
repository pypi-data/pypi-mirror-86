import logging

from src.models.strategy.stategy import Strategy

logger = logging.getLogger(__name__)


class Rolling:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def execute(self) -> bool:
        logger.info(f"Execute rolling with strategy {self.strategy}")

        return self.strategy.execute()
