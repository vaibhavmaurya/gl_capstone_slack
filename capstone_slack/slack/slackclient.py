'''
Reference:
https://github.com/SlackAPI/python-slack-sdk#getting-started-tutorial
https://slack.dev/python-slack-sdk/web/index.html


https://api.slack.com/tools/python-slack-events-api

'''

__all__ = ['get_slack_client', 'CHANNEL']

import os
from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError



'''
By default load_dotenv will look for the .env file 
in the current working directory or any parent directories 
however you can also specify the path if your particular 
use case requires it be stored elsewhere.
'''

CHANNEL = f"#{os.getenv('SLACK_CHANNEL')}"

def get_slack_client():
    '''
        Return the Slack Webclient
    '''
    return WebClient(os.getenv('SLACK_TOKEN'))