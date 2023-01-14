'''
Reference:
https://www.youtube.com/watch?v=6gHvqXrfjuo&t=343s

https://github.com/slackapi/python-slack-events-api

One can use bolt
https://slack.dev/bolt-python/tutorial/getting-started
https://github.com/slackapi/bolt-python/tree/main/examples


interactive messages
https://github.com/slackapi/python-message-menu-example

https://slack.dev/python-slack-sdk/web/index.html#conversations

ngrok http <port number>


TODO:

Lets use bolt instead

https://slack.dev/bolt-python/tutorial/getting-started



https://ae80-122-171-20-219.in.ngrok.io/slack/events

'''

from flask import Flask

from dotenv import load_dotenv
load_dotenv()


from slackeventsapi import SlackEventAdapter
import os
from slack_communication import slack_send_message, SlackCommError
import json
from flask import request
import requests



SIGNING_SECRET = os.getenv('SIGNING_SECRET')

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET,'/slack/events', app)


'''
Start with your slack events adapter
'''

# Respond on message
def respond():
    pass


def get_json_ask():
    '''
        Read ask.json file to be used for slack response
    '''
    with open(os.getenv('ASK_JSON_FILE'), 'r') as f:
        return json.load(f)


# Create an event listener for "reaction_added" events and print the emoji name
# @slack_event_adapter.on("reaction_added")
# def reaction_added(event_data):
#     print(event_data)



@slack_event_adapter.on('message')
def on_message(payload):
    print("I am called")
    send_message = True
    event = payload.get('event', {})

    print(event)
    channel_id, user_id, bot_id = event.get('channel'), event.get('user'), event.get('bot_id')
    # print(f'''
    #     Your user: {user_id}
    #     Channel: {channel_id}
    # ''')
    # if channel matches with the required channel
    # Ignore any response comes from Bot itself
    if os.getenv('SLACK_CHANNEL_ID') != channel_id or \
        os.getenv('BOT_USER_ID') == user_id:
        # exit here
        send_message = False
    # 'user': 'U04GY8CTTLH'
    # 'bot_id': 'B04GKK4DGBU'
    # 'channel': 'C04GCV8DANA'

    # BOT_USER_ID=U04GY8CTTLH
    # BOT_ID=B04GKK4DGBU
    # SLACK_CHANNEL_ID=C04GCV8DANA
    if os.getenv('SLACK_CHANNEL_ID') == channel_id and os.getenv('BOT_USER_ID') == user_id:
        print("SAME CHANNEL")
        send_message = False

    if send_message:
        text = event.get('text')
        print(f'''
            Message from channel: {channel_id}:
            {text}
        ''')

        # Follow this reference
        # https://api.slack.com/legacy/interactive-messages

        slack_send_message('Try block', blocks=get_json_ask()["blocks"])
    



################################## Handle Interaction ######################################## 

# Refrence
# https://github.com/slackapi/python-message-menu-example


# Let's handle the confirm button press
# Complete flow is here

# find the conform action
def find_action(action_id, actions) -> True:
    return any(x['action_id'] == action_id for x in actions)


def retrieve_values(states_values: dict) -> dict:
    all_action_ids = get_json_ask()["action_elements"]
    payload = {}
    for _, v in states_values.items():
        for action_id, action_val in v.items():
            if action_id in all_action_ids:
                if action_val['type'] == 'static_select':
                    payload[action_id] = action_val['selected_option']['value']
                elif action_val['type'] == 'plain_text_input':
                    payload[action_id] = action_val['value']
    # print(payload)
    return payload



def get_model_response(input):
    req_url = os.getenv('NLPMODELSERVICE')
    data = {
        "Countries": input["country"],
        "Local": "Local_03",
        "Industry Sector": "Mining",
        "Accident Level": "I",
        "Potential Accident Level": "III",
        "Genre": input["gender"],
        "Employee or Third Party": "Employee",
        "Critical Risk": "Others",
        "Description": input["incident"]    
        }

    # print(f'''
    #     Check the input data:
    #     {data}
    # ''')

    res = requests.post(req_url, json = data)
    risk_rate = res.json()['answer']
    # print(f'''
    #     Response got from the data
    #     {res.json()}
    # ''')

    return f'''
    There is a potential risk of {risk_rate}
    '''



@app.route('/slack/message-actions', methods=['POST'])
def incoming_slack_message():
    print("Action is called")
    form_json = json.loads(request.form["payload"])
    # .. do something with the req ..
    if find_action(os.getenv('CONFIRM_ACTION_ID'), form_json['actions']):
        # print(form_json)
        # slack_send_message('Your message is captured')
        res = retrieve_values(form_json['state']['values'])
        final_res = get_model_response(res)
        slack_send_message(final_res, thread_ts=form_json['message']['ts'])
        # slack_send_message(final_res, thread_ts=None)
        # slack_send_message(final_res)
    return 'action successful'


@app.route('/slack/message-options', methods=['POST', 'OPTIONS'])
def incoming_slack_options():
    # .. idk ..
    return 'ok'




if __name__ == '__main__':
    app.run(debug=True,port=os.getenv('PORT'), host="0.0.0.0")
