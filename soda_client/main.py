import asyncio
import functools
import inspect
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import aiohttp


class Soda:
    def __init__(self, host=None, token=None, threshold=None,
                 project_name=None, max_workers=4, max_connectors=20,
                 session_factory=aiohttp.ClientSession
                 ):
        connector = aiohttp.TCPConnector(limit=max_connectors)
        self.loop = asyncio.get_event_loop()
        self.client_session = session_factory(
            loop=self.loop,
            connector=connector,
            headers={
                "Authorization": F"Basic {token}"
            })
        self.project_name = project_name
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.stack = defaultdict(dict)
        self.server_url = host
        self.threshold = threshold

    async def report(self, data):
        time_elapsed = data['end'] - data['start']
        if time_elapsed > self.threshold:
            await self.client_session.post(self.server_url, json=data)
        else:
            pass

    def profile(self, func):

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def timer(*args, **kwargs):
                start = time.time()
                result = await func(*args, **kwargs)
                end = time.time()

                await self.report({
                    "name": func.__qualname__,
                    "start": start,
                    "end": end,
                    "arguments": func.__code__.co_varnames,
                    "call_params": {"args": args, "kwargs": kwargs},
                    "type": "coroutine function",
                    "project_name": self.project_name
                })
                return result

            return timer
        else:
            @functools.wraps(func)
            def timer(*args, **kwargs):
                start = time.time()
                called_at = datetime.now().timestamp()
                result = func(*args, **kwargs)
                end = time.time()
                self.loop.run_until_complete(self.report({
                    "called_at": called_at,
                    "name": func.__qualname__,
                    "start": start,
                    "end": end,
                    "arguments": func.__code__.co_varnames,
                    "call_params": {"args": args, "kwargs": kwargs},
                    "type": "function",
                    "project_name": self.project_name
                }))
                return result

            return timer
