import sys

if 'redisgears' not in sys.modules:
    from .placeholders import (   # noqa: F401
        atomic, execute, hashtag, log,
        gearsConfigGet, configGet,
        GearsBuilder, GB,
    )
