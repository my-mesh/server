DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS node;
DROP TABLE IF EXISTS data;

PRAGMA foreign_keys = ON;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE node (
  node_id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  mesh_id INTEGER UNIQUE,
  type TEXT NOT NULL,
  active INTEGER DEFAULT 0
);

CREATE TABLE data (
  data_id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  payload TEXT,
  node_id INTEGER NOT NULL,
  FOREIGN KEY (node_id) REFERENCES node(node_id)
);