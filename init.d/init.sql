CREATE TABLE IF NOT EXISTS crawl.page (
  id int AUTO_INCREMENT,
  url varchar(255) NOT NULL UNIQUE,
  
  INDEX parent_url (url),
  PRIMARY KEY(id)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS crawl.link (
  url varchar(255) NOT NULL,
  status int NOT NULL,
  parent_id int NOT NULL,
  link_text varchar(255),

  PRIMARY KEY(url),
  FOREIGN KEY (parent_id)
    REFERENCES page(id)  
) ENGINE = InnoDB;