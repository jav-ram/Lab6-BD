SELECT COUNT(DISTINCT b.ItemID) FROM DescriptionCategory b WHERE b.ItemID IN(SELECT ic.ItemID FROM DescriptionCategory as ic GROUP BY ic.ItemID HAVING count(ic.CategoryID) == 4);
