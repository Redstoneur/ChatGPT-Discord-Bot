def deleteChannel(discord_channel_id: int) -> str:
    """
    Delete a channel
    :param discord_channel_id: channel id
    :return: None
    """
    return f"DELETE FROM channels WHERE discord_channel_id = {discord_channel_id};"
