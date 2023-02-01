# ChatGPT-Discord-Bot

## Introduction

Ce projet est un bot discord permettant de communiquer avec le modèle de langue OpenAI via un canal Discord. Les
informations sur les utilisateurs et les conversations sont stockées dans une base de données MySQL pour permettre au
bot de se souvenir des conversations précédentes.

## Prérequis

Pour utiliser ce projet, vous devez avoir les éléments suivants installés sur votre machine:

- Docker
- Docker Compose

## Installation

Clonez ce dépôt sur votre machine local.

```bash
git clone https://github.com/Redstoneur/chatGPT-discord-bot.git
```

Ouvrez un terminal dans le répertoire du projet cloné.

Créez un fichier .env à la racine du projet et y incluez les variables d'environnement suivantes:

```makefile
OPENAI_API_KEY=
MYSQL_HOST=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB_NAME=
OPENAI_ENGINE=
DISCORD_BOT_TOKEN=
PREFIX_COMMAND=
```

Exécutez la commande suivante pour démarrer le projet avec Docker Compose:

```bash
docker-compose up
```

## Utilisation

Une fois l'installation terminée, le bot sera en ligne et prêt à communiquer avec les utilisateurs via des canaux
Discord autorisés. Les administrateurs peuvent utiliser la commande !addchannel pour autoriser un canal à être utilisé
par le bot. Les utilisateurs seront ajoutés à la base de données lors de leur première conversation avec le bot.

## Conclusion

Ce projet est un bot de conversation simple mais puissant basé sur le modèle de langue OpenAI et capable de se souvenir
des conversations précédentes grâce à une base de données MySQL. Il peut être facilement utilisé et déployé à l'aide de
Docker Compose.