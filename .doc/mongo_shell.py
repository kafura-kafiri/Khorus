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

[
            {
                "$match": query
            },
            {
                "$lookup": {
                    "localField": "*",
                    "from": foreign,
                    "foreignField": "*",
                    "as": "{}_{}".format(self.collection.name, foreign)
                }
            },
            {
                "$group": group
            }
        ]