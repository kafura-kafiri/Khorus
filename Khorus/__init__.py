from Khorus.talk2choori import free_users, hot_orders, init_road
from Khorus.algorithm import compute_roads
from time import sleep
from Khorus.notification import ack_notif


def job():
    users = free_users()
    orders = hot_orders()
    matches = compute_roads(users, orders)
    for road, _ids in matches:
        init_road(road)
        ack_notif(road, _ids)


while True:
    job()
    sleep(10)