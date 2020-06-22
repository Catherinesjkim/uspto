-- -----------------------------------------------------
-- Table uspto.GRANT_SUMMARY
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.METRICS_G (
  `GrantID` VARCHAR(20) NOT NULL,
  `ForwardCitCnt` INT DEFAULT NULL,
  `BackwardCitCnt` INT DEFAULT NULL,
  `TCT` INT DEFAULT NULL,
  PRIMARY KEY (`GrantID`))
  ENGINE = InnoDB;

--
-- Method 1: Insert statement
--
INSERT INTO uspto.METRICS_G (`GrantId`, `ForwardCitCnt`, `BackwardCitCnt`)
SELECT a.GrantID, count(c.CitedID), count(b.GrantID)
FROM uspto.GRANT as a
JOIN uspto.GRACIT_G as b ON
a.GrantID=b.GrantID
JOIN uspto.GRACIT_G as c ON
a.GrantID=c.CitedID
GROUP BY a.GrantID;

--
-- Method 2: Update Statement
--

INSERT INTO uspto.METRICS_G (`GrantID`) SELECT `GrantID` FROM uspto.GRANT;

UPDATE uspto.METRICS_G, (select CitedID, count(*) as count from uspto.GRACIT_G group by GrantID) as t2
SET    uspto.METRICS_G.ForwardCitCnt = t2.count
WHERE  uspto.METRICS_G.GrantID = t2.CitedID;

UPDATE uspto.METRICS_G, (select GrantID, count(*) as count from uspto.GRACIT_G group by GrantID) as t2
SET    uspto.METRICS_G.BackwardCitCnt = t2.count
WHERE  uspto.METRICS_G.GrantID = t2.GrantID;
