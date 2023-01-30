import os
import discord
import mysql.connector
import openai
from typing import Tuple

# RequestDB
from RequestDB.insert import *
from RequestDB.select import *

# Required environment variables
required_env_vars = [
    "OPENAI_API_KEY",
    "MYSQL_HOST",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DB_NAME",
    "OPENAI_ENGINE",
    "DISCORD_BOT_TOKEN"
]

# Store environment variables in a dictionary
env_vars = {}
for var in required_env_vars:
    value = os.environ.get(var)
    if value is None:
        raise Exception(f"Missing required environment variable: {var}")
    env_vars[var] = value

# Set API key for OpenAI
openai.api_key = env_vars["OPENAI_API_KEY"]

# Connect to MySQL database
mydb = mysql.connector.connect(
    host=env_vars["MYSQL_HOST"],
    user=env_vars["MYSQL_USER"],
    password=env_vars["MYSQL_PASSWORD"],
    database=env_vars["MYSQL_DB_NAME"]
)

# Create a cursor for the database connection
mycursor = mydb.cursor()


# Def Request server sql
def RequestServerSQL(request: str) -> None:
    """
    Request to the server sql
    :param request: request to the server sql
    :return: None
    """
    mycursor.execute(request)
    mydb.commit()


def RequestServerSQLFetch(request: str) -> list:
    """
    Request to the server sql
    :param request: request to the server sql
    :return: None
    """
    mycursor.execute(request)
    mydb.commit()
    return mycursor.fetchall()


RequestServerSQL("""
CREATE TABLE if not exists users
(
    discord_user_id INT PRIMARY KEY NOT NULL,
    username        VARCHAR(255)    NOT NULL
);
""")
RequestServerSQL("""
CREATE TABLE if not exists servers
(
    discord_server_id INT PRIMARY KEY NOT NULL,
    server_name       VARCHAR(255)    NOT NULL
);
""")
RequestServerSQL("""
CREATE TABLE if not exists inservers
(
    discord_user_id   INT NOT NULL REFERENCES users (discord_user_id),
    discord_server_id INT NOT NULL REFERENCES servers (discord_server_id),
    PRIMARY KEY (discord_user_id, discord_server_id)
);
""")
RequestServerSQL("""
CREATE TABLE if not exists channels
(
    discord_channel_id INT PRIMARY KEY NOT NULL,
    channel_name       VARCHAR(255)    NOT NULL,
    server_id          VARCHAR(255)    NOT NULL REFERENCES servers (discord_server_id)
);
""")
RequestServerSQL("""
CREATE TABLE if not exists conversation_history
(
    conversation_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id         INT             NOT NULL,
    channel_id      INT             NOT NULL,
    message         TEXT            NOT NULL,
    reponse         TEXT            NULL,
    timestamp       DATETIME        NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (discord_user_id),
    FOREIGN KEY (channel_id) REFERENCES channels (discord_channel_id)
);
""")


# Discord Client class
class MyClient(discord.Client):

    def channels_allowed(self, discord_server_id) -> list:
        # Get the list of channels from the database
        myresult: list = RequestServerSQLFetch(listChannelsServer(discord_server_id))
        # Return the list of channels
        return [channel[0] for channel in myresult]

    async def on_ready(self) -> None:
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return

        # verify if the user is in the database
        if RequestServerSQLFetch(existUser(message.author.id))[0][0] == 0:
            RequestServerSQL(insertUser(message.author.id, message.author.name))

            # verify if the server is in the database
            if RequestServerSQLFetch(existServer(message.guild.id))[0][0] == 0:
                RequestServerSQL(insertServer(message.guild.id, message.guild.name))

            RequestServerSQL(insertUserInServer(message.author.id, message.guild.id))
        # verify if the user is in the server
        elif message.guild.id not in RequestServerSQLFetch(serverIdOfUser(message.author.id)):
            RequestServerSQL(insertUserInServer(message.author.id, message.guild.id))

        if message.content.startswith("!test") and message.author.permissions_in(message.channel).administrator:
            await message.channel.send("test")
        elif message.content.startswith("!listChannels"):
            result: str = "The list of channels is: "
            for channel in self.channels_allowed(message.guild.id):
                result += f"{channel}, "
            # Remove the last comma
            result = result[:-2]
            await message.channel.send(result)
        # Add a new channel command
        elif message.content.startswith("!addChannel") and message.author.permissions_in(message.channel).administrator:
            # Get the channel ID
            channel_id: str = message.content.split(" ")[1] if len(message.content.split(" ")) > 1 else str(
                message.channel.id)

            channel: discord.TextChannel = self.get_channel(int(channel_id))
            if channel is None:
                await message.channel.send(f"Channel {channel_id} not found.")
                return

            # Add the channel to the list of allowed channels
            RequestServerSQL(insertChannel(channel.id, channel.name, message.guild.id))

            # Confirm to the user that the channel was added
            await message.channel.send(f"Channel {channel.name} added.")
        else:
            # Check if the channel is allowed
            if message.channel.id in self.channels_allowed(message.guild.id):
                # Use OpenAI to generate a response
                response: str = openai.Completion.create(
                    engine=env_vars["OPENAI_ENGINE"],
                    prompt="User: " + message.content,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                ).choices[0].text

                # Add the conversation to the database
                mycursor.execute(
                    insertConversation_history(message.author.id, message.channel.id, message.content, response))
                mydb.commit()

                # Send the response back to Discord
                await message.channel.send("Bot: " + response)


# intents de connexion
intents = discord.Intents.default()  # default, all but presences and member caching
intents.message_content = True  # permet de récupérer le contenu des messages
# intents = discord.Intents.all()  # pour tout les intents

# Create the Discord client
client = MyClient(intents=intents)

# Start the Discord client
client.run(env_vars["DISCORD_BOT_TOKEN"])
