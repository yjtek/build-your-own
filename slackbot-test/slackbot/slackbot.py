import os
import time
import re

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from flask import Flask, request

from utils.secrets import get_secret
from utils.message_kit import (
    post_regular_message,
    post_ephemeral_message,
    post_block_formatted_message,
    find_channel,
    pull_messages_from_oldest_to_latest,
)

import logging
from logging import Logger
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.WARN)
logger: Logger = logging.getLogger('gai-slackbot-logger')

SLACK_BOT_TOKEN: str = get_secret('bot_user_oauth_token')
OPENAI_TOKEN: str = get_secret('slackbot_openai_svc_acct_secretkey')
MY_SLACK_USER_ID: str = get_secret('yj_slack_user_id')

client = WebClient(token=SLACK_BOT_TOKEN)
SLACK_CHANNEL_ID: str = find_channel(client=client, channel_name='20240601-gai-slackbot-test') #get_secret('slack_channel_id')

# post_regular_message(client=client, channel_id=SLACK_CHANNEL_ID, message='hello :wave:')
# post_ephemeral_message(client=client, channel_id=SLACK_CHANNEL_ID, user_id=MY_SLACK_USER_ID, message='hello 123')
# post_block_formatted_message(client=client, channel_id=SLACK_CHANNEL_ID, blocks=[{
#     "type": "section",
#     "text": {
#         "type": "mrkdwn",
#         "text": "Danny Torrence left the following review for your property:"
#     }
# }])
# print(pull_messages_from_oldest_to_latest(
#     client=client, channel_id=SLACK_CHANNEL_ID,
#     latest_unixts=time.time(), oldest_unixts=time.time() - (24*60*60*7)
# ))
