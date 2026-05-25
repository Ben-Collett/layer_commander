from krita import DockWidget,  Node
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from .layer_monitor import LayerMonitor
from .layer_utils import get_position
from .commands import bulk_execute
from .logger import Logger
from .dialogs import display_error


class LayerCommander(DockWidget):
    def __init__(self):
        super().__init__()
        self.active_node: Node | None = None
        self.monitor = LayerMonitor(self.update_active_layer_name)
        self.setWindowTitle("Layer Commander")
        self.logger = Logger(display_error)

        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.text_field = QTextEdit()
        layout.addWidget(self.text_field)

        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self.execute_command)
        layout.addWidget(self.execute_btn)

        self.setWidget(widget)
        self.monitor.refresh()

    def _get_command_box_str(self):
        return self.text_field.toPlainText()

    def update_active_layer_name(self, nodes):
        if len(nodes) > 0:
            node = nodes[0]
            self.active_node = nodes[0]
            name = node.name()
            x, y = get_position(node)
            self.label.setText(f"Active layer: {name} {x} {y}")
        else:
            self.active_node = None

    def execute_command(self):
        if self.active_node:
            lines = self._get_command_box_str().replace("\r\n", "\n").split("\n")
            bulk_execute(lines, self.logger, self.active_node)

    def canvasChanged(self, _):
        self.monitor.refresh()
