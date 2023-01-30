def insertUser(discord_user_id: int, username: str) -> str:
    """
    Insert a user in the database
    :param discord_user_id: id of the user
    :param username: name of the user
    :return: str of the request
    """
    return f"INSERT INTO users (discord_id, username) VALUES ({discord_user_id}, '{username}')"


def insertServer(discord_server_id: int, server_name: str) -> str:
    """
    Insert a server in the database
    :param discord_server_id: id of the server
    :param server_name: name of the server
    :return: str of the request
    """
    return f"INSERT INTO servers (discord_id, server_name) VALUES ({discord_server_id}, '{server_name}')"


def insertUserInServer(discord_server_id: int, discord_user_id: int) -> str:
    """
    Insert a server in the database
    :param discord_server_id: id of the server
    :param discord_user_id: id of the user
    :return: str of the request
    """
    return f"INSERT INTO inservers (server_id, user_id) VALUES ({discord_server_id}, {discord_user_id})"

def insertChannel(discord_channel_id: int, channel_name: str, discord_server_id: int) -> str:
    """
    Insert a channel in the database
    :param discord_channel_id: id of the channel
    :param channel_name: name of the channel
    :param discord_server_id: id of the server
    :return: str of the request
    """
    return f"INSERT INTO channels (discord_id, channel_name, server_id) VALUES ({discord_channel_id}, '{channel_name}', {discord_server_id})"


def insertConversation_history(discord_user_id: int, discord_channel_id: int, message: str, response: str) -> str:
    """
    Insert a conversation in the database
    :param discord_user_id: id of the user
    :param discord_channel_id: id of the channel
    :param message: message of the user
    :return: str of the request
    """
    return f"INSERT INTO conversation_history (user_id, channel_id, message, response) VALUES ({discord_user_id}, {discord_channel_id}, '{message}', '{response}')"



