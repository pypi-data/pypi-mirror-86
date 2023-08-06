import sys

if 'redisgears' not in sys.modules:
    from .placeholders import (   # noqa: F401
        atomic,
        execute,
        hashtag,
        configGet,
        gearsConfigGet,
        log,
        GearsBuilder,
        GB,
    )
else:
    from redisgears import atomicCtx as atomic  # noqa: F401
    from redisgears import executeCommand as execute  # noqa: F401
    from redisgears import getMyHashTag as hashtag  # noqa: F401
    from redisgears import config_get as configGet  # noqa: F401

    log
    gearsConfigGet
    GearsBuilder
    GB
