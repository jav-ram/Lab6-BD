SELECT count(DISTINCT u.UserID) FROM Item as i, User as u, Bid as b WHERE i.UserID = u.UserID AND b.UserID = i.UserID;
