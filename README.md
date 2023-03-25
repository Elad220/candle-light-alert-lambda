# Candle Lighting Alert Lambda

This lambda takes the alert bot's token and all the chat ids who started a conversation with it, and
when the lambda scheduler schedules their run, it alerts the users when the candle lighting time is due.

## Requirements

1. 1. Install the Python requirements using Poetry, then zip the lambda before upload
2. The following environment variables are necessary for the lambda to execute properly:

    a. BOT_TOKEN - the token of the Telegram bot created

    b. BOT_CHATID - the ID of the user who started a conversation with the bot, it's necessary for sending a message back to them. This environment variable is updated automatically by the poller bot.