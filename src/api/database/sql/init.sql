-- schema for the table


CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL, 
  category VARCHAR NOT NULL, 
  content TEXT NOT NULL,
  embedding vector(3)
);

INSERT INTO articles (title, category, content, embedding) 
SELECT 'test', 'data for pg', 'init', '[1,2,3]'
WHERE NOT EXISTS (SELECT 1 FROM ARTICLES LIMIT 1);
