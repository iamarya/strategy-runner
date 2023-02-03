class Watcher:
    def __init__(self) -> None:
        self.values = list()

    def next(self, tick):
        self.values.append(tick)

    def print(self):
        print(self.values)
