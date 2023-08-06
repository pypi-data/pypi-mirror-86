class Strategy:
    def __str__(self) -> str:
        return type(self).__name__

    def execute(self) -> bool:
        return False
