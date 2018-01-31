from gcm import GCM
gcm = GCM("")


def ack_notif(road, order_ids):
    token = road['user']['gcm']
    gcm.json_request(registration_ids=[token], data={"orders": order_ids, "road": road['_id'], })