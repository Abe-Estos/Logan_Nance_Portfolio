CREATE DATABASE horrorbuzzchatbot;
USE horrorbuzzchatbot;

CREATE TABLE basic_ask (
      keyword varchar(255) NOT NULL,
      info varchar(255),
      PRIMARY KEY (keyword)
);

CREATE TABLE article_ask (
      article_name varchar(255) NOT NULL,
      info varchar(255),
      date TIMESTAMP,
      author varchar(255),
      media_type ENUM('movie','game','theatre','news','event','other'),
      PRIMARY KEY (article_name)
);

INSERT INTO basic_ask(keyword,info)
VALUES('horrorbuzz','Horrorbuzz is a news-site focused on horror media, including movies, games and theatre.');

INSERT INTO article_ask(article_name,info, date, author, media_type)
VALUES('Strawberry Cubes A Glitchy, Morbid Game','A review on the game strawberry cubes which is a surreal lofi game with a focus on glitches and an uneasy atmosphere.',  TIMESTAMP("2016-01-27",  "12:10:11"), "Wes Conan", 'game');