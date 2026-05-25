from krita import Node, Krita, Document
from .document_utils import get_document_size
import math
from PyQt6.QtCore import QPointF


def _get_moved_amount(node: Node) -> tuple[int, int]:
    pnt = node.position()
    x = pnt.x()
    y = pnt.y()
    return x, y


def get_position(node: Node) -> tuple[int, int]:
    pnt = node.bounds()
    return pnt.x(), pnt.y()


def get_size(node: Node) -> tuple[int, int]:
    sz = node.bounds()
    return sz.width(), sz.height()


def move_center_to(node: Node, x: int, y: int):
    # offset by width/2,height/2
    width, height = get_size(node)
    width //= 2
    height //= 2
    move_to(node, x-width, y-height)


def center(node: Node, doc_width: int, doc_height: int):
    move_center_to(node, doc_width//2, doc_height//2)


def rotate(node: Node, degrees: int):
    rotation = math.radians(degrees)
    node.rotateNode(rotation)


def move_by(node: Node, dx: int, dy: int):
    moved_x, moved_y = _get_moved_amount(node)
    node.move(moved_x+dx, moved_y+dy)


def move_to(node: Node, x: int, y: int):
    real_x, real_y = get_position(node)
    moved_x, moved_y = _get_moved_amount(node)
    unmoved_x, unmoved_y = real_x-moved_x, real_y-moved_y
    x -= unmoved_x
    y -= unmoved_y
    node.move(x, y)


def duplicate_node_above(node: Node) -> Node | None:
    """Duplicate a node and place the copy above the original in the hierarchy.
    Args:
        node: The Node to duplicate.
    Returns:
        The duplicated Node, or None if duplication failed.
    """
    parent = node.parentNode()
    if parent is None:
        return None
    dup = node.duplicate()
    if dup is None:
        return None
    parent.addChildNode(dup, node)
    return dup


def flip_horizontal(layer: Node):
    bounds = layer.bounds()
    center = QPointF(
        bounds.x() + bounds.width() / 2,
        bounds.y() + bounds.height() / 2,
    )
    layer.scaleNode(center, -bounds.width(), bounds.height(), "Bicubic")


def flip_vertical(layer: Node):
    bounds = layer.bounds()
    center = QPointF(
        bounds.x() + bounds.width() / 2,
        bounds.y() + bounds.height() / 2,
    )
    layer.scaleNode(center, bounds.width(), -bounds.height(), "Bicubic")
