var idVen = db.Item.distinct("seller");
db.User.count({$and:[{_id:{$in:idVen}},{"$where":"this.rating>1000"}]})
