var idVen = db.Item.distinct("seller");
var idBid = db.Item.distinct("bids.bidder_id");
db.User.count({$and:[{_id:{$in:idVen}},{_id:{$in:idBid}}]})
