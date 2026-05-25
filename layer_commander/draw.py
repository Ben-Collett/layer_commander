from krita import Krita, Document
from PyQt6.QtCore import QRectF, QPointF, QPoint, QRect


def _expand_to_fit(node, bounds: QRectF):
    doc = Krita.instance().activeDocument()
    if not doc:
        return

    node_bounds = node.bounds()
    if node_bounds.isEmpty():
        return

    x, y = int(bounds.x()), int(bounds.y())
    w, h = int(bounds.width()), int(bounds.height())
    needed = QRect(x, y, w, h)

    if node_bounds.contains(needed):
        return

    new_x = min(node_bounds.x(), x)
    new_y = min(node_bounds.y(), y)
    new_right = max(node_bounds.x() + node_bounds.width(), x + w)
    new_h = max(node_bounds.y() + node_bounds.height(), y + h)
    new_w = new_right - new_x

    doc_bounds = doc.bounds()
    if (new_x < doc_bounds.x() or new_y < doc_bounds.y()
            or new_x + new_w > doc_bounds.x() + doc_bounds.width()
            or new_y + new_h > doc_bounds.y() + doc_bounds.height()):
        dnx = min(doc_bounds.x(), new_x)
        dny = min(doc_bounds.y(), new_y)
        dnr = max(doc_bounds.x() + doc_bounds.width(), new_x + new_w)
        dnb = max(doc_bounds.y() + doc_bounds.height(), new_y + new_h)
        doc.resizeImage(dnx, dny, dnr - dnx, dnb - dny)

    node.cropNode(new_x, new_y, new_w, new_h)


def draw_circle(node, doc: Document, x, y, radius_x, radius_y=None):
    if radius_y is None:
        radius_y = radius_x
    needed = QRectF(x - radius_x, y - radius_y, radius_x * 2, radius_y * 2)
    _expand_to_fit(node, needed)
    node.paintEllipse(needed)


def draw_line(node, doc: Document, x1, y1, x2, y2):
    doc = Krita.instance().activeDocument()
    if not doc:
        return
    padding = 5
    min_x = min(x1, x2) - padding
    min_y = min(y1, y2) - padding
    max_x = max(x1, x2) + padding
    max_y = max(y1, y2) + padding
    needed = QRectF(min_x, min_y, max_x - min_x, max_y - min_y)
    _expand_to_fit(node, needed)
    node.paintLine(QPoint(int(x1), int(y1)), QPoint(int(x2), int(y2)))
