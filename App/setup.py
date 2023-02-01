import os
import discord
import mysql.connector
import openai
from typing import Tuple

# RequestDB
from RequestDB import *
from RequestDB.insert import *
from RequestDB.select import *
from RequestDB.delete import *

# Required environment variables
required_env_vars = [
    "OPENAI_API_KEY",
    "MYSQL_HOST",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DB_NAME",
    "OPENAI_ENGINE",
    "DISCORD_BOT_TOKEN",
    "PREFIX_COMMAND"
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


def RequestsServerSQL(requests: str, separator: str = ";") -> None:
    """
    Requests to the server sql
    :param requests: requests to the server sql
    :param separator: separator of the requests
    :return: None
    """
    requests: list = requests.split(separator)
    for request in requests:
        print(request)
        try:
            RequestServerSQL(request=request)
        except Exception as e:
            print(request + "\n" +
                  "Error: " + str(e))


def RequestServerSQLFetch(request: str) -> list:
    """
    Request to the server sql
    :param request: request to the server sql
    :return: None
    """
    mycursor.execute(request)
    return mycursor.fetchall()


def RequestServerSQLFetchListList(request: str) -> list:
    """
    Request to the server sql
    :param request: request to the server sql
    :return: None
    """
    res: list = []
    for row in RequestServerSQLFetch(request=request):
        res.append(list(row))
    return res


RequestsServerSQL(requests="""
CREATE TABLE if not exists users
(
    discord_user_id BIGINT PRIMARY KEY NOT NULL,
    username        VARCHAR(255)       NOT NULL
);
CREATE TABLE if not exists servers
(
    discord_server_id BIGINT PRIMARY KEY NOT NULL,
    server_name       VARCHAR(255)       NOT NULL
);
CREATE TABLE if not exists inservers
(
    discord_user_id   BIGINT NOT NULL REFERENCES users (discord_user_id) ON DELETE CASCADE,
    discord_server_id BIGINT NOT NULL REFERENCES servers (discord_server_id) ON DELETE CASCADE,
    PRIMARY KEY (discord_user_id, discord_server_id)
);
CREATE TABLE if not exists channels
(
    discord_channel_id BIGINT PRIMARY KEY NOT NULL,
    channel_name       VARCHAR(255)       NOT NULL,
    discord_server_id          VARCHAR(255)    NOT NULL REFERENCES servers (discord_server_id) ON DELETE CASCADE
);
CREATE TABLE if not exists conversation_history
(
    conversation_id     BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    discord_user_id     BIGINT             NOT NULL,
    discord_channel_id  BIGINT             NOT NULL,
    message             TEXT               NOT NULL,
    response            TEXT               DEFAULT NULL,
    timestamp           DATETIME           NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (discord_user_id) REFERENCES users (discord_user_id) ON DELETE CASCADE,
    FOREIGN KEY (discord_channel_id) REFERENCES channels (discord_channel_id) ON DELETE CASCADE
);
""")


# Discord Client class
class MyClient(discord.Client):

    async def channels_allowed_ID(self, discord_server_id) -> list:
        # Get the list of channels from the database
        myresult: list = RequestServerSQLFetch(request=
                                               listIDChannelsServer(discord_server_id=discord_server_id)
                                               )
        # Return the list of channels
        return [channel[0] for channel in myresult]

    async def channels_allowed_Name(self, discord_server_id) -> list:
        # Get the list of channels from the database
        myresult: list = RequestServerSQLFetch(request=
                                               listNameChannelsServer(discord_server_id=discord_server_id)
                                               )
        # Return the list of channels
        return [channel[0] for channel in myresult]

    async def linkToServeur(self, message: discord.Message) -> bool:
        """
        Check if the user is in the server
        :param message: message
        :return: True if the user is in the server
        """
        # Get the list of id of the server from the database
        myresult: list = RequestServerSQLFetch(request=
                                               serverIdOfUser(discord_user_id=message.author.id)
                                               )
        # Return if the server is in the list
        return message.guild.id in [server[0] for server in myresult]

    async def isAdmin(self, message: discord.Message, commande: bool = False) -> bool:
        """
        Check if the user is an administrator
        :param message: message
        :param commande: if the command is a command
        :return: True if the user is an administrator
        """
        for role in message.author.roles:
            if role.permissions.administrator:
                if commande:
                    await message.channel.send(message.author.mention + "\nVous êtes administrateur !")
                return True
        if commande:
            await message.channel.send(message.author.mention + "\n Vous n'êtes pas administrateur !")
        return False

    async def on_ready(self) -> None:
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return None

        # verify if the user is in the database
        if RequestServerSQLFetchListList(request=existUser(discord_user_id=message.author.id))[0][0] == 0:
            RequestServerSQL(request=
                             insertUser(discord_user_id=message.author.id,
                                        username=message.author.name)
                             )
        # verify if the server is in the database
        if RequestServerSQLFetchListList(request=existServer(discord_server_id=message.guild.id))[0][0] == 0:
            RequestServerSQL(request=
                             insertServer(discord_server_id=message.guild.id,
                                          server_name=message.guild.name))
        # verify if the user is in the server
        if not await self.linkToServeur(message=message):
            RequestServerSQL(request=
                             insertUserInServer(discord_server_id=message.guild.id,
                                                discord_user_id=message.author.id)
                             )

        # Test command
        if message.content.startswith(env_vars["PREFIX_COMMAND"] + "test") and await self.isAdmin(message):
            await message.channel.send("test")
        # List the channels command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "listChannels"):
            result: str = "The list of channels is: "
            for channel in await self.channels_allowed_Name(message.guild.id):
                result += f"{channel}, "
            # Remove the last comma
            result = result[:-2]
            await message.channel.send(result)
        # Add a new channel command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "addChannel") and await self.isAdmin(message):
            # Get the channel ID
            channel_id: str = message.content.split(" ")[1] if len(message.content.split(" ")) > 1 else str(
                message.channel.id)

            channel: discord.TextChannel = self.get_channel(int(channel_id))
            if channel is None:
                await message.channel.send(f"Channel {channel_id} not found.")
                return

            # Add the channel to the list of allowed channels
            RequestServerSQL(request=
                             insertChannel(discord_channel_id=channel.id,
                                           channel_name=channel.name,
                                           discord_server_id=message.guild.id)
                             )

            # Confirm to the user that the channel was added
            await message.channel.send(f"Channel {channel.name} added.")
        # Remove a channel command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "removeChannel") and await self.isAdmin(message):
            # Get the channel ID
            channel_id: str = message.content.split(" ")[1] if len(message.content.split(" ")) > 1 else str(
                message.channel.id)

            channel: discord.TextChannel = self.get_channel(int(channel_id))
            if channel is None:
                await message.channel.send(f"Channel {channel_id} not found.")
                return

            # Remove the channel from the list of allowed channels
            RequestServerSQL(request=deleteChannel(discord_channel_id=channel.id))

            # Confirm to the user that the channel was removed
            await message.channel.send(f"Channel {channel.name} removed.")
        # help command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "help"):
            result: str = "The list of commands is: "
            listCommande: list = [
                {"command": "test", "description": "Test if the bot is working", "admin": True},
                {"command": "listChannels", "description": "List all the channels where the bot can answer",
                 "admin": False},
                {"command": "addChannel",
                 "description": "Add a channel to the list of channels where the bot can answer",
                 "admin": True},
                {"command": "removeChannel",
                 "description": "Remove a channel from the list of channels where the bot can answer",
                 "admin": True},
                {"command": "help", "description": "List all the commands", "admin": False}
            ]
            for commande in listCommande:
                if commande["admin"]:
                    if await self.isAdmin(message):
                        result += f"\n{env_vars['PREFIX_COMMAND']}{commande['command']} : {commande['description']}"
                else:
                    result += f"\n{env_vars['PREFIX_COMMAND']}{commande['command']} : {commande['description']}"
            await message.channel.send(result)
        # If the message is not a command
        else:
            # Check if the channel is allowed
            if message.channel.id in await self.channels_allowed_ID(message.guild.id):
                # Use OpenAI to generate a response
                try:
                    response: str = openai.Completion.create(
                        engine=env_vars["OPENAI_ENGINE"],
                        prompt=message.content,
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    ).choices[0].text
                except Exception as e:
                    print(e)
                    response: str = "Error: OpenAI API is not responding.\n" \
                                    "Please try again later."

                # Add the conversation to the database
                RequestServerSQL(request=
                                 insertConversation_history(discord_user_id=message.author.id,
                                                            discord_channel_id=message.channel.id,
                                                            message=turnOffApostrophe(message.content),
                                                            response=turnOffApostrophe(response))
                                 )

                # Send the response back to Discord
                await message.channel.send("Bot:\n" + response)

        return None


# intents de connexion
intents = discord.Intents.default()  # default, all but presences and member caching
intents.message_content = True  # permet de récupérer le contenu des messages
# intents = discord.Intents.all()  # pour tout les intents

# Create the Discord client
client = MyClient(intents=intents)

# Start the Discord client
client.run(token=env_vars["DISCORD_BOT_TOKEN"])
