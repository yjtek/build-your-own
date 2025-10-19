from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse

import time
from typing import TypedDict

import logging
from logging import Logger
logger: Logger = logging.getLogger('gai-slackbot-msg-kit-logger')

Message = TypedDict('Message', {'user': str | None, 'ts': str | None, 'thread_ts': str | None, 'text': str | None})

def post_regular_message(client: WebClient, message: str, channel_id: str):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
    except SlackApiError as e:
        assert e.response["error"]

def post_ephemeral_message(client: WebClient, message: str, channel_id: str, user_id: str):
    try:
        response: SlackResponse = client.chat_postEphemeral(
            channel=channel_id,
            text=message,
            user=user_id,
        )
    except SlackApiError as e:
        assert e.response["error"]

def post_block_formatted_message(client: WebClient, blocks: list[dict], channel_id: str):
    '''
    For complex payloads, prototype with https://api.slack.com/tools/block-kit-builder
    '''
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            blocks=blocks
        )
    except SlackApiError as e:
        assert e.response["error"]

def find_channel(client: WebClient, channel_name: str) -> str:
    try:
        # Call the conversations.list method using the WebClient
        for result in client.conversations_list():
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    conversation_id = channel["id"]
                    return conversation_id
                
        return ''

    except SlackApiError as e:
        return ''
    
def _process_message(client: WebClient, channel_id: str, message: dict) -> Message | list[Message]:
    if not message.get('thread_ts'):
        return _parse_single_message(message)
    return _parse_message_thread(client, channel_id, message)

def _parse_single_message(message: dict) -> Message:
    return Message(
        user = message.get('user'),
        ts = message.get('ts'),
        thread_ts = message.get('thread_ts'),
        text = message.get('text'),
    )

def _parse_message_thread(client: WebClient, channel_id: str, message: dict) -> list[Message]:
    replies = client.conversations_replies(
        channel=channel_id,
        ts = message.get('thread_ts', '')
    )
    # return replies.get('messages')
    parse_replies = [_parse_single_message(x) for x in replies.get('messages', [])]
    return parse_replies

def pull_messages_from_oldest_to_latest(
    client: WebClient, 
    channel_id: str, 
    oldest_unixts: float, 
    latest_unixts: float
) -> list[Message | list[Message]]:
    result = client.conversations_history(
        channel=channel_id, 
        latest=str(latest_unixts), 
        oldest=str(oldest_unixts)
    )
    ## Get all top level messages
    root_messages: list[dict] = result.get('messages', [{}])
    processed_messages = [_process_message(client, channel_id, x) for x in root_messages]
    return processed_messages