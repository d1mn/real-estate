from typing import List
import time


async def retry(func, args: List[object], times: int, sleep_ms: int):
    exception = None
    for _ in range(times):
        try:
            res = await func(*args)
        except Exception as e:
            exception = e
            time.sleep(sleep_ms / 1000)
            continue
        return res
    raise exception
