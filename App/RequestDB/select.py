def existUser(discord_user_id: int) -> str:
    """
    Check if the user is in the database
    :param discord_user_id: id of the user
    :return: str of the request
    """
    return f"SELECT count(*)>0 FROM users WHERE discord_user_id = {discord_user_id}"


def existServer(discord_server_id: int) -> str:
    """
    Check if the server is in the database
    :param discord_server_id: id of the server
    :return: str of the request
    """
    return f"SELECT count(*)>0 FROM servers WHERE discord_server_id = {discord_server_id}"


def serverIdOfUser(discord_user_id: int) -> str:
    """
    Get the server id of a user
    :param discord_user_id: id of the user
    :return: str of the request
    """
    return f"SELECT discord_server_id FROM inservers WHERE discord_user_id = {discord_user_id}"

def listIDChannelsServer(discord_server_id: int) -> str:
    """
    List all channels of a server
    :param discord_server_id: id of the server
    :return: str of the request
    """
    return f"SELECT discord_channel_id FROM channels WHERE discord_server_id = {discord_server_id}"


def listNameChannelsServer(discord_server_id: int) -> str:
    """
    List all channels of a server
    :param discord_server_id: id of the server
    :return: str of the request
    """
    return f"SELECT channel_name FROM channels WHERE discord_server_id = {discord_server_id}"

