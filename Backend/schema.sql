CREATE TABLE `messagingapp`.`user` (
  `userid` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `password` VARCHAR(160) NOT NULL,
  `emailid` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `emailid_UNIQUE` (`emailid` ASC));

  CREATE TABLE `messagingapp`.`messages` (
  `messageId` INT NOT NULL AUTO_INCREMENT,
  `sourceUID` INT NOT NULL,
  `destinationUID` INT NOT NULL,
  `sha512Hash` VARCHAR(600) NOT NULL,
  PRIMARY KEY (`messageId`));

ALTER TABLE `messagingapp`.`messages` 
ADD COLUMN `messageTimeEpoch` VARCHAR(200) NOT NULL AFTER `sha512Hash`;

ALTER TABLE `messagingapp`.`messages` 
ADD COLUMN `message` VARCHAR(2000) NOT NULL AFTER `messageTimeEpoch`;



