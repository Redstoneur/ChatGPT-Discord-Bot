import os
import discord
import mysql.connector
import openai
from typing import Tuple

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


# Discord Client class
class MyClient(discord.Client):
    async def on_ready(self) -> None:
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return

        # Check if the channel is allowed
        if message.channel.id in channels_allowed:
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
            mycursor.execute("INSERT INTO conversation (user_id, message) VALUES (%s, %s)",
                             (message.author.id, message.content))
            mydb.commit()

            # Send the response back to Discord
            await message.channel.send("Bot: " + response)

        # Add a new channel command
        if message.content.startswith("!addChannel"):
            if message.author.permissions_in(message.channel).administrator:
                # Get the channel ID
                channel_id = message.content.split(" ")[1] if len(message.content.split(" ")) > 1 else str(
                    message.channel.id)

                # Add the channel to the list of allowed channels
                channels_allowed.append(channel_id)

                # Confirm to the user that the channel was added
                await message.channel.send(f"Channel {channel_id} has been added.")


# Create the Discord client
client = MyClient()

# Start the Discord client
client.run(env_vars["DISCORD_BOT_TOKEN"])
