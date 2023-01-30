# si la base de données n'existe pas, il faut la créer

CREATE DATABASE if not exists bot_discord;

USE
bot_discord;

CREATE TABLE if not exists users
(
    user_id         INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    discord_user_id VARCHAR(255)    NOT NULL,
    username        VARCHAR(255)    NOT NULL
);

CREATE TABLE if not exists channels
(
    channel_id         INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    discord_channel_id VARCHAR(255)    NOT NULL,
    channel_name       VARCHAR(255)    NOT NULL
);

CREATE TABLE if not exists conversation_history
(
    conversation_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id         INT             NOT NULL,
    channel_id      INT             NOT NULL,
    message         TEXT            NOT NULL,
    timestamp       DATETIME        NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
);
