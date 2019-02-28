CREATE TABLE account (
  id varchar(36),
  nickname varchar(12),
  slug varchar(12),
  PRIMARY KEY account_pk (id),
  UNIQUE KEY nickname_unq (nickname),
  UNIQUE KEY slug_unq (slug)
);