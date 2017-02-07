CREATE TABLE IF NOT EXISTS crawl.page (
  id int AUTO_INCREMENT,
  url varchar(255) NOT NULL UNIQUE,
  previous_url varchar(255) NOT NULL UNIQUE,
  status int NOT NULL,
  parent_id int NOT NULL,
  link_text TEXT,
  state int NOT NULL,

  INDEX idx_url (url),
  INDEX idx_previous_url (previous_url),
  PRIMARY KEY(id)
) ENGINE = INNODB;