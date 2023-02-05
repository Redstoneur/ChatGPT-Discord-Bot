import os
import discord
import mysql.connector
import openai
from typing import Tuple

# Text_Analizor
from Text_Analizor import *

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
    username        VARCHAR(255)       NOT NULL,
    add_date        DATETIME           NOT NULL default CURRENT_TIMESTAMP,
    update_date     DATETIME           NOT NULL default CURRENT_TIMESTAMP
);
CREATE TABLE if not exists servers
(
    discord_server_id BIGINT PRIMARY KEY NOT NULL,
    server_name       VARCHAR(255)       NOT NULL,
    add_date          DATETIME           NOT NULL default CURRENT_TIMESTAMP
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
    discord_server_id          VARCHAR(255)    NOT NULL REFERENCES servers (discord_server_id) ON DELETE CASCADE,
    add_date            DATETIME           NOT NULL default CURRENT_TIMESTAMP
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


# legacy
def Terms_and_Conditions() -> discord.Embed:
    """
    Terms and conditions
    :return: discord.Embed
    """
    terms_and_conditions: discord.Embed = discord.Embed(title="Conditions d'utilisation",
                                                        description="Pour l'utilisation d'un bot Discord permettant "
                                                                    "de communiquer avec ChatGPT",
                                                        color=discord.Color.red())
    terms_and_conditions.add_field(name="1. Utilisation personnelle uniquement",
                                   value="Ce bot est destiné à un usage personnel uniquement et est interdit pour un "
                                         "usage commercial.",
                                   inline=False)
    terms_and_conditions.add_field(name="2. Responsabilité du contenu",
                                   value="Vous êtes responsable de tout contenu que vous publiez ou transmettez via "
                                         "ce bot.",
                                   inline=False)
    terms_and_conditions.add_field(name="3. Contenu répréhensible",
                                   value="Vous vous engagez à ne pas publier ou transmettre de contenu illégal, "
                                         "offensif, diffamatoire, harcelant, menaçant ou autrement répréhensible.",
                                   inline=False)
    terms_and_conditions.add_field(name="4. Suspension de l'accès",
                                   value="Le créateur du bot Discord se réserve le droit de suspendre votre accès à "
                                         "ce bot si vous ne respectez pas les conditions d'utilisation.",
                                   inline=False)
    terms_and_conditions.add_field(name="5. Responsabilité d'OpenAI",
                                   value="OpenAI n'est pas responsable des erreurs, des inexactitudes ou des dommages "
                                         "causés par l'utilisation de ce bot.",
                                   inline=False)
    terms_and_conditions.add_field(
        name="6. Respect des conditions d'utilisation et politique de confidentialité d'OpenAI",
        value="Vous devez respecter les conditions d'utilisation et la politique de confidentialité d'OpenAI en "
              "vigueur.",
        inline=False)
    terms_and_conditions.add_field(name="7. Modification des conditions d'utilisation",
                                   value="Les conditions d'utilisation peuvent être modifiées à tout moment sans "
                                         "préavis.",
                                   inline=False)
    terms_and_conditions.add_field(name="Acceptation des conditions d'utilisation",
                                   value="L'utilisation de ce bot implique votre acceptation de ces conditions "
                                         "d'utilisation.",
                                   inline=False)

    return terms_and_conditions


# policy
def Privacy_Policy() -> discord.Embed:
    """
    Privacy policy
    :return: discord.Embed
    """
    # bot collect data

    # 1. personal data -> identification data -> discord user id + username + server id + server
    # name + channel id + channel name

    # 2. personal data -> conversation history -> discord user id + discord channel id + message + response + timestamp
    privacy_policy: discord.Embed = discord.Embed(title="Politique de confidentialité",
                                                  description="Pour l'utilisation d'un bot Discord permettant "
                                                              "de communiquer avec ChatGPT",
                                                  color=discord.Color.red())
    privacy_policy.add_field(name="1. Collecte de données :",
                             value="",
                             inline=False)
    privacy_policy.add_field(name="1.1. Données d'identification",
                             value="Le bot collecte les données d'identification suivantes : "
                                   "identifiant utilisateur Discord, nom d'utilisateur Discord, identifiant du serveur "
                                   "Discord, nom du serveur Discord, identifiant du canal Discord, nom du canal "
                                   "Discord.",
                             inline=False)
    privacy_policy.add_field(name="1.2. Historique de conversation",
                             value="Le bot collecte les données suivantes : identifiant utilisateur Discord, "
                                   "identifiant du canal Discord, message, réponse, date et heure.",
                             inline=False)
    privacy_policy.add_field(name="2. Utilisation des données :",
                             value="",
                             inline=False)
    privacy_policy.add_field(name="2.1. Utilisation personnelle",
                             value="L'utilisation des données est destinée à un usage personnel uniquement.",
                             inline=False)
    privacy_policy.add_field(name="2.2. Amélioration du bot",
                             value="Les données sont utilisées pour améliorer le bot.",
                             inline=False)
    privacy_policy.add_field(name="2.3. Partage des données",
                             value="Les données collectées ne sont pas partagées.",
                             inline=False)
    privacy_policy.add_field(name="2.4. Suppression des données",
                             value="Les données collectées sont supprimées après 1 an si vous n'utilisez pas le bot ",
                             # "Les données collectées sont supprimées après 1 an.",
                             inline=False)
    privacy_policy.add_field(name="2.5. Modification de la politique de confidentialité",
                             value="La politique de confidentialité peut être modifiée à tout moment sans préavis.",
                             inline=False)
    privacy_policy.add_field(name="2.6. Acceptation de la politique de confidentialité",
                             value="L'utilisation de ce bot implique votre acceptation de cette politique de "
                                   "confidentialité.",
                             inline=False)
    return privacy_policy


def legacy() -> discord.Embed:
    """
    Create the legacy embed
    :return:
    """
    terms_and_conditions: discord.Embed = Terms_and_Conditions()
    privacy_policy: discord.Embed = Privacy_Policy()

    terms_and_conditions_Dict: dict = terms_and_conditions.to_dict()
    privacy_policy_Dict: dict = privacy_policy.to_dict()

    terms_and_conditions_text: str = json.dumps(terms_and_conditions_Dict)
    privacy_policy_text: str = json.dumps(privacy_policy_Dict)

    # fusion of the two embeds
    legacy: discord.Embed = discord.Embed(title="Conditions d'utilisation et politique de confidentialité",
                                          description="",
                                          color=discord.Color.red())
    legacy.add_field(name="Conditions d'utilisation",
                     value=terms_and_conditions_text,
                     inline=False)
    legacy.add_field(name="Politique de confidentialité",
                     value=privacy_policy_text,
                     inline=False)
    return legacy


# Bad words
list_Bad_Words: List_Bad_Words = List_Bad_Words(json_file_links_bad_words="Data/JSON/Bad_Word.json")


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

        # message is a alone mention of the bot (without command)

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

        # hello command : message is alone mention of the bot (without command) or a command hello
        if message.content == "<@" + str(self.user.id) + ">" or \
                (message.content == env_vars["PREFIX_COMMAND"] + "hello" and await self.isAdmin(message)) or \
                (message.content.startswith(env_vars["PREFIX_COMMAND"] + "hello") and await self.isAdmin(message)):
            await message.reply("Bonjour !\n"
                                "Pour avoir la liste des commandes, tapez `" + env_vars["PREFIX_COMMAND"] + "help`\n" +
                                "Pour avoir les informations sur la politique de confidentialité, tapez `" +
                                env_vars["PREFIX_COMMAND"] + "privacyPolicy`\n" +
                                "Pour avoir les conditions générales d'utilisation, tapez `" +
                                env_vars["PREFIX_COMMAND"] + "termsAndConditions`\n" +
                                "Pour avoir les informations sur la politique de confidentialité et les conditions "
                                "générales, tapez `" +
                                env_vars["PREFIX_COMMAND"] + "legacy`",
                                mention_author=False)
            return None
        # quit command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "quit") and await self.isAdmin(message):
            await message.reply("Au revoir !")
            await self.close()
            return None
        # privacy policy command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "privacyPolicy"):
            await message.reply(embed=Privacy_Policy())
            return None
        # terms and conditions command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "termsAndConditions"):
            await message.reply(embed=Terms_and_Conditions())
            return None
        # legacy command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "legacy"):
            await message.reply(embed=legacy())
            return None
        # List the channels command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "listChannels"):
            result: str = "The list of channels is: "
            for channel in await self.channels_allowed_Name(message.guild.id):
                result += f"{channel}, "
            # Remove the last comma
            result = result[:-2]
            await message.reply(result)
        # Add a new channel command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "addChannel") and await self.isAdmin(message):
            # Get the channel ID
            channel_id: str = message.content.split(" ")[1] if len(message.content.split(" ")) > 1 else str(
                message.channel.id)

            channel: discord.TextChannel = self.get_channel(int(channel_id))
            if channel is None:
                await message.reply(f"Channel {channel_id} not found.")
                return

            # Add the channel to the list of allowed channels
            RequestServerSQL(request=
                             insertChannel(discord_channel_id=channel.id,
                                           channel_name=channel.name,
                                           discord_server_id=message.guild.id)
                             )

            # Confirm to the user that the channel was added
            await message.reply(f"Channel {channel.name} added.")
        # Remove a channel command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "removeChannel") and await self.isAdmin(message):
            # Get the channel ID
            channel_id: str = message.content.split(" ")[1] if len(message.content.split(" ")) > 1 else str(
                message.channel.id)

            channel: discord.TextChannel = self.get_channel(int(channel_id))
            if channel is None:
                await message.reply(f"Channel {channel_id} not found.")
                return

            # Remove the channel from the list of allowed channels
            RequestServerSQL(request=deleteChannel(discord_channel_id=channel.id))

            # Confirm to the user that the channel was removed
            await message.reply(f"Channel {channel.name} removed.")
        # help command
        elif message.content.startswith(env_vars["PREFIX_COMMAND"] + "help"):
            result: str = "The list of commands is: "
            listCommande: list = [
                {"command": "hello", "description": "Say hello to the bot", "admin": False},
                {"command": "quit", "description": "Quit the bot", "admin": True},
                {"command": "privacyPolicy", "description": "Show the privacy policy", "admin": False},
                {"command": "termsAndConditions", "description": "Show the terms and conditions", "admin": False},
                {"command": "legacy", "description": "Show the legacy", "admin": False},
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
            await message.reply(result)
        # If the message is not a command
        else:
            # Check if the channel is allowed
            if message.channel.id in await self.channels_allowed_ID(message.guild.id):
                # Check if the message contains a bad word
                if list_Bad_Words.check_bad_words(message.content):
                    await message.reply("Your message contains a bad word.")
                    return None

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
                await message.reply("Bot:\n" + response)

        return None


# intents de connexion
intents = discord.Intents.default()  # default, all but presences and member caching
intents.message_content = True  # permet de récupérer le contenu des messages
# intents = discord.Intents.all()  # pour tout les intents

# Create the Discord client
client = MyClient(intents=intents)

# Start the Discord client
client.run(token=env_vars["DISCORD_BOT_TOKEN"])
