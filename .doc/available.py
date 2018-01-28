a = [
    {
        "$match": {
            "$and": [
                {
                    "privileges.porter.status": 1
                }, {
                    "$or": [
                        {
                            "privileges.porter.shift.lunch": {
                                "$gte": "{{ now }}",
                                "$lt": "{{ now }}"
                            }
                        }, {
                            "privileges.porter.shift.dinner": {
                                "$gte": "{{ now }}",
                                "$lt": "{{ now }}"
                            }
                        }
                    ]
                }, {
                    "username": {
                        "$nin": "$busies"
                    }
                }
            ]
        }
    }, {
        "lookup": {
            "from": "orders",
            "let": {
                "order_item": "$item",
                "order_qty": "$ordered"
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "status": {
                                "$neq": "delivered"
                            }
                        }
                    }
                }, {
                    "$project": {
                        "busies": {
                            "$push": "$username"
                        }
                    }
                }
            ],
            "as": "busy"
        }
    }
]
