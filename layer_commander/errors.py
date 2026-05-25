from .result import Result


def _format_dimension_error(dimension: str, res: Result) -> str | None:
    if res.err_msg:
        return f"couldn't parse {dimension}, reason: {res.err_msg}"

    return None


def format_dimension_errors(args: list[str], dimensions: dict[str, Result]) -> str | None:
    errors = []
    for name, res in dimensions.items():
        if res.err_msg is not None:
            errors.append(_format_dimension_error(name, res))

    if len(errors) == 0:
        return None
    elif len(errors) == 1:
        error = "error"
    else:
        error = "errors"

    err_msg = f"parse {error} in {" ".join(args)}:\n"

    for err in error:
        err_msg += f"\t{err}\n"

    return err_msg.removesuffix("\n")
