from krita import Krita
from krita import QObject, QTimer


class LayerMonitor(QObject):
    def __init__(self, callback, interval_ms=500):
        super().__init__()
        self._callback = callback
        self._last_node_ids = set()
        self._timer = QTimer()
        self._timer.timeout.connect(self.refresh)

        if interval_ms >= 0:
            self._timer.start(interval_ms)

        self.refresh()

    def set_interval(self, interval_ms):
        if interval_ms < 0:
            self._timer.stop()
        else:
            self._timer.start(interval_ms)

    def refresh(self):
        window = Krita.instance().activeWindow()
        if window is None:
            return
        view = window.activeView()
        if view is None:
            return

        nodes = view.selectedNodes()
        current_ids = {node.uniqueId() for node in nodes}

        if current_ids != self._last_node_ids:
            self._last_node_ids = current_ids
        self._callback(nodes)

    def stop(self):
        self._timer.stop()

    def start(self, interval_ms=None):
        if interval_ms is not None and interval_ms >= 0:
            self._timer.start(interval_ms)
        elif self._timer.interval() > 0 or interval_ms == 0:
            self._timer.start()
