-- -----------------------------------------------------
-- Table uspto.GRANT_SUMMARY
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.METRICS_G (
  `GrantID` VARCHAR(20) DEFAULT NULL,
  `ForwardCitCnt` INT DEFAULT NULL,
  `BackwardCitCnt` INT DEFAULT NULL,
  `TCT` INT DEFAULT NULL,
  PRIMARY KEY (`GrantID`))
  ENGINE = InnoDB;

--
-- Method 1: Insert statement
--
INSERT INTO uspto.PATCIT_COUNT_G (`GrantId`, `ForwardCitCnt`, `BackwardCitCnt`)
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
UPDATE uspto.METRICS_G
SET
ForwardCitCnt = (
SELECT count(b.CitedID)
FROM uspto.GRANT as a
JOIN uspto.GRACIT_G as b ON
a.GrantID=b.CitedID
GROUP BY a.GrantID
)
WHERE 1=1;

UPDATE uspto.METRICS_G
SET
BackwardCitCnt = (
SELECT count(b.CitedID)
FROM uspto.GRANT as a
JOIN uspto.GRACIT_G as b ON
a.GrantID=b.GrantID
GROUP BY a.GrantID
)
WHERE 1=1;
