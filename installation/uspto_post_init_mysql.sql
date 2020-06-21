-- -----------------------------------------------------
-- Table uspto.GRANT_SUMMARY
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.PATCIT_COUNT_G (
  `GrantID` VARCHAR(20) NOT NULL,
   `fw_cit_cnt` INT NOT NULL,
   `bw_cit_cnt` INT NOT NULL,
  PRIMARY KEY (`GrantID`))
  ENGINE = InnoDB;
