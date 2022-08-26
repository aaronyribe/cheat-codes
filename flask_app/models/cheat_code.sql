-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema cheat_code_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cheat_code_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cheat_code_schema` DEFAULT CHARACTER SET utf8 ;
USE `cheat_code_schema` ;

-- -----------------------------------------------------
-- Table `cheat_code_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheat_code_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cheat_code_schema`.`games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheat_code_schema`.`games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `release_year` YEAR(4) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cheat_code_schema`.`cheat_codes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheat_code_schema`.`cheat_codes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` TEXT(255) NOT NULL,
  `game_id` INT NOT NULL,
  `submitted_by` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_cheat_codes_games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_cheat_codes_users1_idx` (`submitted_by` ASC) VISIBLE,
  CONSTRAINT `fk_cheat_codes_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `cheat_code_schema`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cheat_codes_users1`
    FOREIGN KEY (`submitted_by`)
    REFERENCES `cheat_code_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cheat_code_schema`.`verified`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheat_code_schema`.`verified` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `verified` TINYINT NULL,
  `user_id` INT NOT NULL,
  `cheat_code_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_verified_cheat_codes1_idx` (`cheat_code_id` ASC) VISIBLE,
  INDEX `fk_verified_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_verified_cheat_codes1`
    FOREIGN KEY (`cheat_code_id`)
    REFERENCES `cheat_code_schema`.`cheat_codes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_verified_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `cheat_code_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
