# exchange publisher
# will send ticks to subscribed agent.

class TickPublisher:

    def __init__(self):
        self.watcher = None

    def subscribe(self, watcher):
        self.watcher = watcher

    def emit(self, tick):
        if self.watcher:
            self.watcher.next(tick)

    def cancel(self):
        self.watcher = None
