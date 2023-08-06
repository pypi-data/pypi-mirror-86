import sys


if 'redisgears' not in sys.modules:
    from .placeholders import (   # noqa: F401
        atomic, execute, hashtag, log,
        gearsConfigGet, configGet,
        GearsBuilder, GB,
    )
else:
    atomic
    execute
    hashtag
    log
    gearsConfigGet
    configGet
    GearsBuilder
    GB

    # from redisgears import atomicCtx as atomic  # noqa: F401
    # from redisgears import executeCommand as execute  # noqa: F401
    # from redisgears import getMyHashTag as hashtag  # noqa: F401
    # from redisgears import log  # noqa: F401
    # from redisgears import config_get as configGet  # noqa: F401

    # def gearsConfigGet(key, default=None):
    #     val = configGet(key)
    #     return val if val is not None else default

    # from redisgears import callNext as call_next
    # from redisgears import registerTimeEvent as registerTE
    # from redisgears import gearsCtx
    # from redisgears import gearsFutureCtx as gearsFuture
    # from redisgears import setGearsSession
    # from redisgears import getGearsSession
    # from redisgears import registerGearsThread
    # from redisgears import isInAtomicBlock
