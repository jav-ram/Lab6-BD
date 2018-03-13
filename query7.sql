var i =db.Item.distinct("category",{"bids.amount":{$gt:100}},{"category":1, "_id":0});
i.length
