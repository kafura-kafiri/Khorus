import requests
khorus_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.' \
             'eyJ1c2VybmFtZSI6Imtob3J1cyIsInByaXZpbGVnZXMiOnsia2hvcnVzIjoiIn19.' \
             'mkSTHLkTgPPv2O_SlpV4clNhKmvdR6mXGLgvSznqzU0'


def free_users():
    response = requests.post("http://localhost:5000/users/frees", data={"key": khorus_key})
    return response.json()


def hot_orders():
    response = requests.post("http://localhost:5000/orders/unassigned", data={"key": khorus_key})
    return response.json()


def init_road():
    pass