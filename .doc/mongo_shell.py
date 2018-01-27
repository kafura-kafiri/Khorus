from pymongo import MongoClient
client = MongoClient()
db = client['test']
orders = db['orders']
orders.aggregate([
    {
      "$match": {
        "status": "A"
      }
    },
    {
      "$group": {
        "_id": "$username",
        "total": {
          "$sum": "$amount"
        }
      }
    }
])

'''s = '''

'''{
                "$lookup": {
                    "from": foreign,
                    "as": "{}_{}".format(self.collection.name, foreign),
                    "pipeline": [
                        {
                            "$match": query,
                        }, {
                            "$group": group
                        }, {
                            "$project": projection
                        }
                    ]
                }
            }'''

b = [
    {

    },
]