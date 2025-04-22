-- schema for the table

CREATE TABLE IF NOT EXISTS articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL, 
  category VARCHAR NOT NULL, 
  content TEXT NOT NULL
);

INSERT INTO articles (title, category, content) 
SELECT 'test', 'data for pg', 'init'
WHERE NOT EXISTS (SELECT 1 FROM ARTICLES LIMIT 1);
