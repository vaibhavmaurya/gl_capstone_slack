# NLP Capstone Project Deployment 
---
[git repository](https://github.com/vaibhavmaurya/gl_capstone_slack.git)

# Table of contents

- [Overview](#overview)
- [Slack Communication Service](#slack-communication-service)
  - [Slack Communication Service implementation references](#slack-communication-service-implementation-references)
- [ML Model training and predcition service](#ml-model-training-and-predcition-service)

## Overview
For chat/communication, in this project [Slack](slack.com) is being used. There is a bot **gl-nlp-bot** in the slack channel which is used to answer the accident level for any incident reported by user.
How this bot is implemented, detals are below.

This project has two services. Both the services can be deployed in Kubernetes cluster. The respective docker files are avaialble in the repository to build the docker images.
- Slack Communication Service
- ML Model training and prediction service

A brief concept and architecture diagram is below.

![](https://raw.githubusercontent.com/vaibhavmaurya/gl_capstone_slack/main/images/GL_Capstone_Project_Arch.jpg)

- Slack communication service connects with ML Model training and prediction service at port 5010.
- The Slack channel connects with the Slack communication service at port 3010.
- The Slack channel/application creator has to register the service endpoints in the [Slack API portal](api.slack.com)

Below is the snapshot of the bot communication in the slack channel.
![](https://raw.githubusercontent.com/vaibhavmaurya/gl_capstone_slack/master/FullCommunication.jpg)

- First time the member of the slack channel has to invite the **gl-nlp-bot**, which is a bot.
- Once bot is added, the bot will detect the messages posted in the channel.

## Slack Communication Service 
Slack communication service is implemented in Flask, python rest api framework. It has following endpoints

| Service Endpoint | Description |
| ------------------------------------- | ---------------------------------------- |
| `/slack/events` | Whenever there is a message in the channel **gl-capstone-nlp-bot**, this rest api is called by slack. Here the message from the channel is recieved, which is further processed and reply through the bot is prepared here. Bot in response sends back a form, where user has to input the details and click the Confirm button. This communication can be well understood in the below diagram of slack communication snapshot. |
| `/slack/message-actions` | When user clicks the confirm button, the slack channel calls this rest api. Here in this endpoint, data from the user filled form is extracted and passed to **ML model endpoint /predict**. The ML model endpoint responds with the accident level, which is communicated back into the slack channel using bot **gl-nlp-bot** |


### Slack Communication Service implementation references
- [Slack APIs for bot implementation](https://api.slack.com/apis)
- [Slack API developer reference](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/#web-api-client)
- [Create a form to be filled by user](https://api.slack.com/block-kit)

## ML Model training and predcition service
This service is implemented in Flask, python rest api framework. It has following endpoints

| Service Endpoint | Description |
| ------------------------------------- | ---------------------------------------- |
| `/predict` | This endpoint takes the input and predict the potential risk level. |
| `/training` | This endpoint is used to train the model. Here we need to provide the location of the data and the path where data preprocessing and the trained model can be saved as pickle dump. This endpoint is still under construction, though the `training.py` file in the repository is fully functional. |

*Reference input to the service /predict*
```
{
	"Countries": "Country_01",
	"Local": "Local_03",
	"Industry Sector": "Mining",
	"Accident Level": "I",
	"Genre": "Male",
	"Employee or Third Party": "Employee",
	"Critical Risk": "Others",
	"Description": "While installing a segment of the polyurethane pulley protective lyner - 60x4x5cm weighing 1.2 kg - on the head pulley of the ore winch, when the pulley is rotated to compress the lyner inside the channel, it falls from its housing 1.50 m rubbing the right side of the worker hip, generating the injury described."
}
```
