import asyncio

import requests
from soda_client import Soda

response = requests.post("http://0.0.0.0/api/v1.0/auth/", json={
    "email": "test@test.com",
    "password": "test"
}).json()
access_token = response['access_token']

loop = asyncio.get_event_loop()
soda = Soda(access_token, "fib_project")


@soda.profile
async def bad_fib(n):
    if n <= 1:
        return n
    else:
        return (await bad_fib(n - 1) + await bad_fib(n - 2))


loop.run_until_complete(bad_fib(10))
