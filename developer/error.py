class EmailException(Exception):
    def __init__(self, stats: int = None, message: str = None):
        self.stats = stats
        self.message = message
        super().__init__(f"({self.stats}): {self.message}")