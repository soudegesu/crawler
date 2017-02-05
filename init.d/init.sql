CREATE TABLE IF NOT EXISTS crawl.page (
  id int AUTO_INCREMENT,
  url varchar(255) NOT NULL UNIQUE,
  status int NOT NULL,
  parent_id int NOT NULL,
  link_text varchar(255),
  state int NOT NULL,

  INDEX parent_url (url),
  PRIMARY KEY(id)
) ENGINE = INNODB;