__all__ = ['slack_send_message', 'SlackCommError']


'''
    Reference:
    https://api.slack.com/bot-users


    https://api.slack.com/apis

    Create block kit
    Refrence
    https://api.slack.com/block-kit

'''


from slackclient import get_slack_client, CHANNEL
from slack_sdk.errors import SlackApiError


client = get_slack_client()


class SlackCommError(Exception):
    pass



'''

Reference 
https://slack.dev/python-slack-sdk/api-docs/slack_sdk/#web-api-client


    def chat_postMessage(
        self,
        *,
        channel: str,
        text: Optional[str] = None,
        as_user: Optional[bool] = None,
        attachments: Optional[Union[str, Sequence[Union[Dict, Attachment]]]] = None,
        blocks: Optional[Union[str, Sequence[Union[Dict, Block]]]] = None,
        thread_ts: Optional[str] = None,
        reply_broadcast: Optional[bool] = None,
        unfurl_links: Optional[bool] = None,
        unfurl_media: Optional[bool] = None,
        container_id: Optional[str] = None,
        file_annotation: Optional[str] = None,
        icon_emoji: Optional[str] = None,
        icon_url: Optional[str] = None,
        mrkdwn: Optional[bool] = None,
        link_names: Optional[bool] = None,
        username: Optional[str] = None,
        parse: Optional[str] = None,  # none, full
        metadata: Optional[Union[Dict, Metadata]] = None,
        **kwargs,
    )

'''


def slack_send_message(txt: str, blocks=None, thread_ts=None):
    '''
        Send a message to slack channel
    '''
    try:
        print(f'''
        CHANNEL: {CHANNEL}
        ''')
        response = client.chat_postMessage(channel=CHANNEL, text=txt, blocks=blocks, thread_ts=thread_ts)
        assert response["message"]["text"] == txt
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
        raise SlackCommError(f"SLACK_ERROR: {e.response['error']}")



