from pymongo import MongoClient
from Choori.utility import set_password
from copy import deepcopy
from bson import ObjectId
import datetime

client = MongoClient()
db = client['BLOODY_DB']
orders = db['orders']
locations = db['locations']
roads = db['roads']
users = db['users']

user = {
  "username": "",
  "password": "",
  "first_name": "",
  "last_name": "",
  "cellphone": "",
  "salt": "",
  "privileges": {},
  "bank": {
    "name": "",
    "account": "",
    "fee_per_order": "",
    "fixed_salary": ""
  },
  "detail": {
    "probation": "",
    "melli_code": "",
    "birth_date": "",
    "sheba": ""
  }
}

pouria = deepcopy(user)
mohsen = deepcopy(user)
khorus = deepcopy(user)
shahin = deepcopy(user)
pouria['username'] = 'pouria'
pouria['password'] = set_password('sharifi')
pouria['first_name'] = 'pouria'
pouria['last_name'] = 'sharifi'
pouria['cellphone'] = '+989133657623'
pouria['privileges']['dev'] = ''
pouria['privileges']['applicator'] = ''
pouria['bank'] = {}
pouria['detail'] = {}

mohsen['username'] = 'mohsen'
mohsen['password'] = set_password('mohseni')
mohsen['first_name'] = 'mohsen'
mohsen['last_name'] = 'mohseni'
mohsen['cellphone'] = '+989133657623'
mohsen['privileges']['porter'] = {
    "status": 1,
    "shift": {
        "lunch": [0, 1],
        "dinner": [3, 5],
    }
}
mohsen['bank'] = {}
mohsen['detail'] = {}

khorus['username'] = 'khorus'
khorus['password'] = set_password('ququli')
khorus['first_name'] = 'khorus'
khorus['last_name'] = 'ququli'
khorus['cellphone'] = '+989133657623'
khorus['privileges']['khorus'] = ''
khorus['bank'] = {}
khorus['detail'] = {}

shahin['username'] = 'shahin'
shahin['password'] = set_password('qarebaqi')
shahin['first_name'] = 'shahin'
shahin['last_name'] = 'qarebaqi'
shahin['cellphone'] = '+989133657623'
shahin['privileges']['applicator'] = ''
shahin['bank'] = {}
shahin['detail'] = {}

users.delete_many({})
users.insert_many([pouria, mohsen, khorus, shahin])


print([user for user in users.find({})])

order = {
  "object": {
    "code": "911",
    "detail": "sos be zan",
    "#": ["big"]
  },
  "src": [35.787306, 51.415609, "پلاک ۲۰ زیر زمین"],
  "dst": [35.784843, 51.417326, "پلاک ۱ طبقه پنج واحد ۱۰"],
  "status": "[init, auto_dispatched, dispatched, porting, delivered]",
  "delay": 0,
  # "road_id": ObjectId(),
  # "username": "mohsen",
  "applicator": "",
}

_yesterday = datetime.datetime.now() - datetime.timedelta(days=1, hours=1)
jordan_1 = deepcopy(order)

jordan_1['status'] = 'init'
jordan_1['applicator'] = shahin['username']
jordan_1['delay'] = 36 * 60
jordan_1["_date"] = _yesterday
jordan_2 = deepcopy(jordan_1)
jordan_2["_date"] = _yesterday + datetime.timedelta(hours=1)
jordan_2['delay'] = 5 * 60
jordan_3 = deepcopy(jordan_1)
jordan_3["_date"] = _yesterday + datetime.timedelta(days=1)
jordan_3['delay'] = 10 * 60

ferdous_1 = deepcopy(jordan_1)
ferdous_1['applicator'] = pouria['username']
ferdous_1['dst'] = [35.723267, 51.320185, ""]
ferdous_1["_date"] = _yesterday + datetime.timedelta(days=1)

orders.delete_many({})
orders.insert_many([jordan_1, jordan_2, jordan_3, ferdous_1])

print([order for order in orders.find({})])


road = {
    "src": [
        35.787306, 51.415609
    ],
    "dst": [
        35.784843, 51.417326
    ]
}

roads.delete_many({})
roads.insert_one(road)
jordan_1['road_id'] = road['_id']
orders.save(jordan_1)