import requests

from soda_client import Soda

response = requests.post("http://0.0.0.0/api/v1.0/auth/", json={
    "email": "test@test.com",
    "password": "test"
})
print()
access_token = response.json()['access_token']
soda = Soda(access_token, "fib_project")


@soda.profile
def bad_fib(n):
    if n <= 1:
        return n
    else:
        return (bad_fib(n - 1) + bad_fib(n - 2))


bad_fib(5)
