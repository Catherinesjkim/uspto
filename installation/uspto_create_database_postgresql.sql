-- -----------------------------------------------------
-- Create Databse uspto
-- -----------------------------------------------------
DROP DATABASE IF EXISTS uspto;
CREATE DATABASE uspto;

DROP SCHEMA IF EXISTS uspto CASCADE;
CREATE SCHEMA IF NOT EXISTS uspto;

-- -----------------------------------------------------
-- Table uspto.APPLICATION_PAIR
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.APPLICATION_PAIR (
  ApplicationID VARCHAR(20) NOT NULL,
  FileDate DATE DEFAULT NULL,
  AppType VARCHAR(45) DEFAULT NULL,
  ExaminerName VARCHAR(100) DEFAULT NULL,
  GroupArtUnit VARCHAR(45) DEFAULT NULL,
  ConfirmationNum VARCHAR(45) DEFAULT NULL,
  AttorneyDNum VARCHAR(45) DEFAULT NULL,
  ClassSubClass VARCHAR(45) DEFAULT NULL,
  InventorFName VARCHAR(100) DEFAULT NULL,
  CustomerNum VARCHAR(45) DEFAULT NULL,
  Status VARCHAR(200) DEFAULT NULL,
  StatusDate DATE DEFAULT NULL,
  Location VARCHAR(100) DEFAULT NULL,
  LocationDate DATE DEFAULT NULL,
  PubNoEarliest VARCHAR(45) DEFAULT NULL,
  PubDateEarliest DATE DEFAULT NULL,
  PatentNum VARCHAR(45) DEFAULT NULL,
  PatentIssueDate DATE DEFAULT NULL,
  TitleInvention VARCHAR(500) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, FileName));

-- -----------------------------------------------------
-- Table uspto.APPLICATION
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.APPLICATION (
  ApplicationID VARCHAR(20) NOT NULL,
  PublicationID VARCHAR(20) DEFAULT NULL,
  FileDate DATE DEFAULT NULL,
  Kind VARCHAR(2) DEFAULT NULL,
  USSeriesCode VARCHAR(2) DEFAULT NULL,
  AppType VARCHAR(45) DEFAULT NULL,
  PublishDate DATE DEFAULT NULL,
  Title VARCHAR(500) DEFAULT NULL,
  Abstract TEXT DEFAULT NULL,
  ClaimsNum INT DEFAULT NULL,
  DrawingsNum INT DEFAULT NULL,
  FiguresNum INT DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, FileName));

-- -----------------------------------------------------
-- Table uspto.GRANT
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.GRANT (
  GrantID VARCHAR(20) NOT NULL,
  IssueDate DATE DEFAULT NULL,
  Kind VARCHAR(2) DEFAULT NULL,
  USSeriesCode VARCHAR(2) DEFAULT NULL,
  Title VARCHAR(500) DEFAULT NULL,
  Abstract TEXT DEFAULT NULL,
  Claims TEXT DEFAULT NULL,
  ClaimsNum INT DEFAULT NULL,
  DrawingsNum INT DEFAULT NULL,
  FiguresNum INT DEFAULT NULL,
  GrantLength INT DEFAULT NULL,
  ApplicationID VARCHAR(20) DEFAULT NULL,
  FileDate DATE DEFAULT NULL,
  AppType VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, FileName));

-- -----------------------------------------------------
-- Table uspto.INTCLASS_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.INTCLASS_A (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Section VARCHAR(15) DEFAULT NULL,
  Class VARCHAR(15) DEFAULT NULL,
  SubClass VARCHAR(15) DEFAULT NULL,
  MainGroup VARCHAR(15) DEFAULT NULL,
  SubGroup VARCHAR(15) DEFAULT NULL,
  Malformed BOOLEAN DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

  -- -----------------------------------------------------
  -- Table uspto.CPCCLASS_A
  -- -----------------------------------------------------

  CREATE TABLE IF NOT EXISTS uspto.CPCCLASS_A (
    ApplicationID VARCHAR(20) NOT NULL,
    Position INT NOT NULL,
    Section VARCHAR(15) DEFAULT NULL,
    Class VARCHAR(15) DEFAULT NULL,
    SubClass VARCHAR(15) DEFAULT NULL,
    MainGroup VARCHAR(15) DEFAULT NULL,
    SubGroup VARCHAR(15) DEFAULT NULL,
    Malformed BOOLEAN DEFAULT NULL,
    FileName VARCHAR(45),
    PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.USCLASS_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.USCLASS_A (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Class VARCHAR(5) DEFAULT NULL,
  SubClass VARCHAR(15) DEFAULT NULL,
  Malformed BOOLEAN DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.INVENTOR_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.INVENTOR_A (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  FirstName VARCHAR(100) DEFAULT NULL,
  LastName VARCHAR(100) DEFAULT NULL,
  City VARCHAR(100) DEFAULT NULL,
  State VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  Nationality VARCHAR(100) DEFAULT NULL,
  Residence VARCHAR(300) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.ATTORNEY_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.ATTORNEY_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  RegNo VARCHAR(20) DEFAULT NULL,
  FirstName VARCHAR(45) DEFAULT NULL,
  LastName VARCHAR(45) DEFAULT NULL,
  Phone VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.FOREIGNPRIORITY_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.FOREIGNPRIORITY_A (
  ApplicationID VARCHAR(20) NOT NULL,
  DocumentID VARCHAR(100) NOT NULL,
  Position INT NOT NULL,
  Kind VARCHAR(45) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  PriorityDate DATE DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.TRANSACTION
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.TRANSACTION_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Description TEXT DEFAULT NULL,
  Date DATE DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.CORRESPONDENCE
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.CORRESPONDENCE_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Name VARCHAR(100) DEFAULT NULL,
  Address TEXT DEFAULT NULL,
  CustomerNum VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, FileName));

-- -----------------------------------------------------
-- Table uspto.CONTINUITY_PARENT_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.CONTINUITY_PARENT_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Description VARCHAR(100) DEFAULT NULL,
  ParentNum VARCHAR(45) DEFAULT NULL,
  FileDate DATE DEFAULT NULL,
  ParentStatus VARCHAR(45) DEFAULT NULL,
  PatentNum VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.CONTINUITY_CHILD_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.CONTINUITY_CHILD_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Description TEXT DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.ADJUSTMENT_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.ADJUSTMENT_P (
  ApplicationID VARCHAR(20) NOT NULL,
  PriorAfter BOOLEAN DEFAULT NULL,
  FileDate DATE DEFAULT NULL,
  IssueDate DATE DEFAULT NULL,
  PreIssuePetitions VARCHAR(45) DEFAULT NULL,
  PostIssuePetitions VARCHAR(45) DEFAULT NULL,
  USPTOAdjustDays VARCHAR(45) DEFAULT NULL,
  USPTODelayDays VARCHAR(45) DEFAULT NULL,
  ThreeYears VARCHAR(45) DEFAULT NULL,
  APPLDelayDays VARCHAR(45) DEFAULT NULL,
  TotalTermAdjustDays VARCHAR(45) DEFAULT NULL,
  ADelays VARCHAR(45) DEFAULT NULL,
  BDelays VARCHAR(45) DEFAULT NULL,
  CDelays VARCHAR(45) DEFAULT NULL,
  OverlapDays VARCHAR(45) DEFAULT NULL,
  NonOverlapDelays VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PTOManualAdjust VARCHAR(45) DEFAULT NULL);

-- -----------------------------------------------------
-- Table uspto.ADJUSTMENTDESC_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.ADJUSTMENTDESC_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  PriorAfter BOOLEAN DEFAULT NULL,
  Number INT DEFAULT NULL,
  Date DATE DEFAULT NULL,
  ContentDesc TEXT DEFAULT NULL,
  PTODays VARCHAR(45) DEFAULT NULL,
  APPLDays VARCHAR(45) DEFAULT NULL,
  Start VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.EXTENSION_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.EXTENSION_P (
  ApplicationID VARCHAR(20) NOT NULL,
  FileDate DATE DEFAULT NULL,
  USPTOAdjustDays INT DEFAULT NULL,
  USPTODelays INT DEFAULT NULL,
  CorrectDelays INT DEFAULT NULL,
  FileName VARCHAR(45),
  TotalExtensionDays INT DEFAULT NULL);

-- -----------------------------------------------------
-- Table uspto.EXTENSIONDESC_P
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.EXTENSIONDESC_P (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Date DATE DEFAULT NULL,
  Description TEXT DEFAULT NULL,
  PTODays VARCHAR(45) DEFAULT NULL,
  APPLDays VARCHAR(45) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.AGENT_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.AGENT_A (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  OrgName VARCHAR(300) DEFAULT NULL,
  LastName VARCHAR(100) DEFAULT NULL,
  FirstName VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.ASSIGNEE_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.ASSIGNEE_A (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  OrgName VARCHAR(300) DEFAULT NULL,
  Role VARCHAR(45) DEFAULT NULL,
  City VARCHAR(100) DEFAULT NULL,
  State VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.APPLICANT_A
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.APPLICANT_A (
  ApplicationID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  OrgName VARCHAR(300) DEFAULT NULL,
  FirstName VARCHAR(100) DEFAULT NULL,
  LastName VARCHAR(100) DEFAULT NULL,
  City VARCHAR(100) DEFAULT NULL,
  State VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ApplicationID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.USCLASSIFICATION
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.USCLASSIFICATION (
  ClassID INT NOT NULL,
  Class VARCHAR(3) NULL,
  SubClass VARCHAR(6) DEFAULT NULL,
  Indent VARCHAR(2) DEFAULT  NULL,
  SubClassSqsNum VARCHAR(4) DEFAULT NULL,
  NextHigherSub VARCHAR(6) DEFAULT NULL,
  Title VARCHAR(200) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (ClassID, FileName));

-- -----------------------------------------------------
-- Table uspto.INTCLASS_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.INTCLASS_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Section VARCHAR(15) DEFAULT NULL,
  Class VARCHAR(15) DEFAULT NULL,
  SubClass VARCHAR(15) DEFAULT NULL,
  MainGroup VARCHAR(15) DEFAULT NULL,
  SubGroup VARCHAR(15) DEFAULT NULL,
  Malformed BOOLEAN DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.CPCCLASS_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.CPCCLASS_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Section VARCHAR(15) DEFAULT NULL,
  Class VARCHAR(15) DEFAULT NULL,
  SubClass VARCHAR(15) DEFAULT NULL,
  MainGroup VARCHAR(15) DEFAULT NULL,
  SubGroup VARCHAR(15) DEFAULT NULL,
  Malformed BOOLEAN DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.NONPATCIT_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.NONPATCIT_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Citation TEXT DEFAULT NULL,
  Category SMALLINT DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.APPLICANT_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.APPLICANT_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  OrgName VARCHAR(300) DEFAULT NULL,
  FirstName VARCHAR(100) DEFAULT NULL,
  LastName VARCHAR(100) DEFAULT NULL,
  City VARCHAR(100) DEFAULT NULL,
  State VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.INVENTOR_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.INVENTOR_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  FirstName VARCHAR(100) DEFAULT NULL,
  LastName VARCHAR(100) DEFAULT NULL,
  City VARCHAR(100) DEFAULT NULL,
  State VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  Nationality VARCHAR(100) DEFAULT NULL,
  Residence VARCHAR(300) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.USCLASS_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.USCLASS_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  Class VARCHAR(5) DEFAULT NULL,
  SubClass VARCHAR(15) DEFAULT NULL,
  Malformed BOOLEAN DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.AGENT_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.AGENT_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  OrgName VARCHAR(300) DEFAULT NULL,
  LastName VARCHAR(100) DEFAULT NULL,
  FirstName VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.ASSIGNEE_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.ASSIGNEE_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  OrgName VARCHAR(500) DEFAULT NULL,
  Role VARCHAR(45) DEFAULT NULL,
  City VARCHAR(100) DEFAULT NULL,
  State VARCHAR(100) DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.EXAMINER_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.EXAMINER_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  LastName VARCHAR(50) DEFAULT NULL,
  FirstName VARCHAR(50) DEFAULT NULL,
  Department VARCHAR(100) DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.GRACIT_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.GRACIT_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  CitedID VARCHAR(20) DEFAULT NULL,
  Kind VARCHAR(10) DEFAULT NULL,
  Name VARCHAR(100) DEFAULT NULL,
  Date DATE DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  Category SMALLINT DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table uspto.FORPATCIT_G
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.FORPATCIT_G (
  GrantID VARCHAR(20) NOT NULL,
  Position INT NOT NULL,
  CitedID VARCHAR(25) DEFAULT NULL,
  Kind VARCHAR(10) DEFAULT NULL,
  Name VARCHAR(100) DEFAULT NULL,
  Date DATE DEFAULT NULL,
  Country VARCHAR(100) DEFAULT NULL,
  Category SMALLINT DEFAULT NULL,
  FileName VARCHAR(45),
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table `uspto`.`FOREIGNPRIORITY_G`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS uspto.FOREIGNPRIORITY_G (
  GrantID VARCHAR(20) NOT NULL,
  DocumentID VARCHAR(45) NOT NULL,
  Position INT NOT NULL,
  Kind VARCHAR(45) DEFAULT NULL,
  Country VARCHAR(5) DEFAULT NULL,
  PriorityDate DATE DEFAULT NULL,
  FileName VARCHAR(45) NOT NULL,
  PRIMARY KEY (GrantID, Position, FileName));

-- -----------------------------------------------------
-- Table `uspto`.`STARTED_FILES`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS uspto.STARTED_FILES (
  FileName VARCHAR(45),
  PRIMARY KEY (FileName));

-- -----------------------------------------------------
-- Create PostgreSQL Users
-- -----------------------------------------------------

-- Drop user if exists and create a new user with password
DROP USER IF EXISTS uspto;
CREATE USER uspto LOGIN PASSWORD 'Ld58KimTi06v2PnlXTFuLG4';

-- Change the owner of uspto database to uspto user
ALTER DATABASE uspto OWNER TO uspto;

-- Grant privileges to all corresponding databases
GRANT USAGE ON SCHEMA uspto TO uspto;
GRANT ALL ON ALL TABLES IN SCHEMA uspto TO uspto;
