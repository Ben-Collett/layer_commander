import shlex
from typing import Callable
from .result import Result, CommandReturn
from dataclasses import dataclass
from krita import Node, Document
from .document_utils import get_active_document, get_document_size, refresh_projection
from .layer_utils import center, flip_horizontal, flip_vertical,  move_by, move_center_to, move_to, duplicate_node_above, get_position, get_size, rotate
from .dialogs import display_information
from .logger import Logger
from .draw import draw_line, draw_circle
from .errors import format_dimension_errors


def _handle_center(node: Node, document: Document | None,  args: list[str]) -> CommandReturn:
    """
    args should be ["center"] only
    """
    if len(args) != 1:
        return CommandReturn(err_msg="illegal args in center" + str(args))
    if document is None:
        return CommandReturn(err_msg="can't center, no document")
    width, height = get_document_size(document)
    center(node, width, height)
    return CommandReturn()


def _parse_dimension(val: int | str, document_dimension: int | None) -> Result[int]:
    if isinstance(val, int):
        return Result(result=val)

    is_percent = False
    if val.endswith("%"):
        val = val.removesuffix("%")
        is_percent = True
    try:
        extracted_val = float(val)
    except Exception:
        return Result(err_msg=f"couldn't parse {val} as a decimal number")

    if is_percent:
        if not document_dimension:
            return Result(
                err_msg="no document_dimension could't detmermine relative dimension")
        extracted_val /= 100
        extracted_val *= document_dimension

    return Result(result=int(extracted_val))


def _handle_move_by(node: Node, document: Document | None, args: list[str]) -> CommandReturn:
    if len(args) != 3:
        print("illegal arg count in moveby, only two parameters expected", args)
    if document:
        width, height = get_document_size(document)
    else:
        width, height = None, None

    x = _parse_dimension(args[1], width)
    y = _parse_dimension(args[2], height)

    if x.result is None:
        return CommandReturn(err_msg=f"couldn't parse x in moveby {args}, reason:\n\t{x.err_msg}")
    if y.result is None:
        return CommandReturn(err_msg=f"couldn't parse x in moveby {args}, reason:\n\t{y.err_msg}")

    move_by(node, x.result, y.result)
    return CommandReturn()


def _handle_move_to(node: Node, document: Document | None, args: list[str]) -> CommandReturn:
    if len(args) != 3:
        print("illegal arg count in moveto, only two parameters expected", args)
    if document:
        width, height = get_document_size(document)
    else:
        width, height = None, None

    x = _parse_dimension(args[1], width)
    y = _parse_dimension(args[2], height)

    if x.result is None:
        return CommandReturn(err_msg=f"couldn't parse x in move to {args}, reason:\n\t{x.err_msg}")
    if y.result is None:
        return CommandReturn(err_msg=f"couldn't parse x in move to {args}, reason:\n\t{y.err_msg}")

    move_to(node, x.result, y.result)
    return CommandReturn()


def _handle_duplicate(node: Node, _: Document, args: list[str]):
    if len(args) != 1:
        return CommandReturn(err_msg="illegal args in duplicate" + str(args))
    return CommandReturn(new_node=duplicate_node_above(node))


def _handle_move_center_to(node: Node, document: Document, args: list[str]) -> CommandReturn:
    if len(args) != 3:
        print("illegal arg count in move center to, only two parameters expected", args)
    if document:
        width, height = get_document_size(document)
    else:
        width, height = None, None

    x = _parse_dimension(args[1], width)
    y = _parse_dimension(args[2], height)

    msg = format_dimension_errors(args, {"x": x, "y": y})
    if msg:
        return CommandReturn(err_msg=msg)

    move_center_to(node, x.unwrap(), y.unwrap())
    return CommandReturn()


def _handle_help(node: Node, document: Document, _: list[str]) -> CommandReturn:
    lines = []
    if document:
        w, h = get_document_size(document)
        lines.append(f"{document.name()} {w}x{h}")
    else:
        lines.append("no document")
    x, y = get_position(node)
    nw, nh = get_size(node)
    lines.append(command_map.help())
    lines.append(f"current node: {x},{y},{nw},{nh}")
    display_information("\n".join(lines))
    return CommandReturn()


def _handle_rotate(node: Node, _: Document, args: list[str]) -> CommandReturn:
    if len(args) != 2:
        return CommandReturn(err_msg=f"wrong number of args for rotation {args}")

    rotate(node, int(args[1]))
    return CommandReturn()


def _handle_draw_circle(node: Node, document: Document | None, args: list[str]) -> CommandReturn:
    if len(args) not in (4, 5):
        return CommandReturn(f"draw circle arg mismatch: expected <command> x y radius_x optional:radius_y received {args}")
    if document is None:
        return CommandReturn(err_msg="can't draw circle with no document")
    width, height = get_document_size(document)
    x = _parse_dimension(args[1], width)
    y = _parse_dimension(args[2], height)
    radius_x = _parse_dimension(args[3], width)
    radius_y = _parse_dimension(args[4], height) if len(args) == 5 else None
    results = {"x": x, "y": y}

    if radius_y:
        results["radius_x"] = radius_x
        results["radius_y"] = radius_y
    else:
        results["radius"] = radius_x
        radius_y = Result(None)

    draw_circle(node, document, x.unwrap(), y.unwrap(),
                radius_x.unwrap(), radius_y.unwrap())
    return CommandReturn()


def _handle_draw_line(node: Node, document: Document, args: list[str]):
    if len(args) != 5:
        return CommandReturn(err_msg=f"draw line arg mismatch: expected <command> x1 y1  x2 y2, received {args}")
    if document is None:
        return CommandReturn(err_msg="can't draw line with no document")
    width, height = get_document_size(document)
    x1 = _parse_dimension(args[1], width)
    y1 = _parse_dimension(args[2], height)
    x2 = _parse_dimension(args[3], width)
    y2 = _parse_dimension(args[4], height)

    results = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    err_msg = format_dimension_errors(args, results)
    if err_msg:
        return CommandReturn(err_msg=err_msg)

    draw_line(node, document, x1.unwrap(),
              y1.unwrap(), x2.unwrap(), y2.unwrap())
    return CommandReturn()


def _handle_flip_h(node: Node, _: Document | None, args: list[str]):
    if len(args) != 1:
        return CommandReturn(err_msg="flip horizontal arg mismatch: expected no args just <command>, received {args}")
    flip_horizontal(node)
    return CommandReturn()


def _handle_flip_v(node: Node, _: Document | None, args: list[str]):
    if len(args) != 1:
        return CommandReturn(err_msg="flip vertical arg mismatch: expected no args just <command>, received {args}")
    flip_vertical(node)
    return CommandReturn()


@dataclass
class Command:
    name: str
    description: str
    callback: Callable


class CommandMap:
    def __init__(self):
        self.commands = [
            Command(
                "moveby", "moveby x y: moves the current layer by x y pixels.", _handle_move_by),
            Command("mvb", "mvb x y: alias for moveby", _handle_move_by),
            Command(
                "moveto", "moveto x y: moves the current layer to a given x y in the canvas.", _handle_move_to),
            Command("mvt", "mvt x y: alias for moveto", _handle_move_to),
            Command(
                "center", "center: centers the current layer in the document.", _handle_center),
            Command("cen", "cen: alias for center", _handle_center),
            Command(
                "duplicate", "duplicate: duplicates the current layer above.", _handle_duplicate),
            Command("dup", "dup: alias for duplicate", _handle_duplicate),
            Command("movecenterto", "movecenterto x y: moves the center of the current layer to a given x y.",
                    _handle_move_center_to),
            Command("mvc", "mvc x y: alias for movecenterto",
                    _handle_move_center_to),
            Command(
                "rotate", "rotate deg: rotates the current layer by deg degrees.", _handle_rotate),
            Command("rot", "rot deg: alias for rotate", _handle_rotate),
            Command("fliphorizontal",
                    "fliphorizontal: flips layer horizontally", _handle_flip_h),
            Command("flh",
                    "flh: alias for fliphorizontal", _handle_flip_h),
            Command("flipvertical",
                    "fliphorizontal: flips layer horizontally", _handle_flip_v),
            Command("flv",
                    "flv: alias for flipvertical", _handle_flip_v),
            Command(
                "circle", "circle x y radius_x [radius_y]: draws a circle on the current layer.", _handle_draw_circle),
            Command(
                "cir", "cir x y radius_x [radius_y]: alias for circle", _handle_draw_circle),
            Command(
                "line", "line x1 y1 x2 y2: draws a line on the current layer.", _handle_draw_line),
            Command("lin", "lin x1 y1 x2 y2: alias for line", _handle_draw_line),
            Command("help", "help: displays help information.", _handle_help),
            Command("h", "h: alias for help", _handle_help),
        ]
        self.cmd_map = {}
        for command in self.commands:
            self.cmd_map[command.name] = command.callback

    def help(self) -> str:
        lines = [
            "NOTE: unless other wise noted all parameters can be in pixels or as a percentage of a canvas size",
            "for example: in a 200 by 200 grid moveto 100 100 is the same as moveto 50% 50%",
        ]

        for command in self.commands:
            lines.append(command.description)

        return "\n".join(lines)


command_map = CommandMap()


def bulk_execute(lines: list[str], logger: Logger, node: Node):

    cmd_map = command_map.cmd_map
    document = get_active_document()
    messages: list[str] = []
    for line in lines:
        parsed = shlex.split(line, comments=True)
        if len(parsed) == 0:
            continue
        if parsed[0] not in cmd_map:
            messages.append(f"unknown command: {parsed[0]}")
            continue

        result: CommandReturn = cmd_map[parsed[0]](node, document, parsed)

        if result.new_node:
            node = result.new_node
        if result.err_msg:
            messages.append(result.err_msg)

    if len(messages) > 0:
        logger.log("\n".join(messages))

    if document:
        refresh_projection(document)
