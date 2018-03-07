DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Country;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS DescriptionCategory;
DROP TABLE IF EXISTS Category;

CREATE TABLE Item (
	ItemID 		int,
	UserID 		varchar[25],
	Name 		varchar[15],
	Currently	varchar[20],
	First_bid	varchar[20],	
	started		date,
	ends		date,
	buy_price	varchar[20],
	Description	varchar[1000],
	PRIMARY KEY (ItemID),
	FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE User (
	UserID 		varchar[25],
	Rating		int,
	CountryID	int,
	Location varchar[20],
	PRIMARY KEY(UserID),
	FOREIGN KEY(CountryID) REFERENCES Country(CountryID)
);

CREATE TABLE Country (
	CountryID 	int,
	name		varchar[20],
	PRIMARY KEY(CountryID)
);

CREATE TABLE Bid (
	BidID		int,
	ItemID 	int,
	UserID		int,
	Time		datetime,
	Amount	varchar[20],
	PRIMARY KEY(BidID),
	FOREIGN KEY(ItemID) REFERENCES Item(ItemID),
	FOREIGN KEY(UserID) REFERENCES User(UserID)	
);

CREATE TABLE DescriptionCategory(
	ItemID 	int,
	CategoryID	int
);

CREATE TABLE Category (
	CategoryID	int,
	Nombre	varchar[20],
	PRIMARY KEY(CategoryID)
);
