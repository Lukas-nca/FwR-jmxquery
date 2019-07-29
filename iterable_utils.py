from tqdm import trange
import time


def call_periodicaly(function, period_seconds=120, max_calls=float('inf')):
    count = 1
    while count <= max_calls:
        try:
            print("\nNext call in:")
            tsleep(period_seconds)
            function()
            count += 1
        except KeyboardInterrupt as ki:
            print("keyboard interrupt. exiting...")
            exit(0)


def tsleep(seconds: int):
    if seconds > 0:
        for _ in trange(seconds):
            time.sleep(1)


def flatten(l):
    """
    >>> list(flatten([]))
    []
    >>> list(flatten([1, 2, 3]))
    [1, 2, 3]
    >>> list(flatten([1, 2, [3, 4]]))
    [1, 2, 3, 4]
    >>> list(flatten([[1, 2], [3, 4]]))
    [1, 2, 3, 4]
    >>> list(flatten([[1, 2], [3, 4, [5, 6]]]))
    [1, 2, 3, 4, 5, 6]
    >>> list(flatten(['1', 2, 3]))
    ['1', 2, 3]
    >>> list(flatten(['1', 2, '[3, 4]']))
    ['1', 2, '[3, 4]']
    >>> list(flatten([['1', 2], ['3, 4']]))
    ['1', 2, '3, 4']
    >>> list(flatten([['1', 2], [3, 4, [5, 6]]]))
    ['1', 2, 3, 4, 5, 6]
    >>> list(flatten('adsf'))
    ['adsf']
    >>> list(flatten(['adsf', 'adsf', [1, 2, {3, 4}, [5]], (6, 7, ['wert'])]))
    ['adsf', 'adsf', 1, 2, 3, 4, 5, 6, 7, 'wert']
    """
    if isinstance(l, str):
        yield l
    else:
        for e in l:
            if isinstance(e, str) or not hasattr(e, '__iter__'):
                yield e
            else:
                for innerE in flatten(e):
                    yield innerE
