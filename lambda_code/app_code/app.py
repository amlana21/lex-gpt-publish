
import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging
import openai

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)





def close(session_attributes, fulfillment_state, message,intent_name,response_text):
    response={
                'sessionState':{
                # 'sessionAttributes':sessionAttributes,
                'dialogAction':{
                    'type':'Close',
                    'fulfillmentState':'Fulfilled'
                },
                'intent': {
                    'confirmationState': 'Confirmed',
                    'name': intent_name,
                    'state': 'Fulfilled'
                }
            },
            'messages': [{'contentType': 'PlainText', 'content': response_text}]
            }

    return response




def evaluate_openai(txtvalue):
    openai.api_key = os.getenv("GPT_API_KEY")
    text_to_assess=txtvalue
    prompt_txt=f'classify whether this sentence sentiment is positive or negative.reply in same line. Here is the sentence: \n\n"{text_to_assess}"'
    openai_response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_txt,
      temperature=0,
      max_tokens=60,
      top_p=1.0,
      frequency_penalty=0.5,
      presence_penalty=0.0
    )
    print(openai_response)
    return openai_response['choices'][0]['text']

def evaluate_sentiment(intent_request):
    text_to_assess=intent_request['interpretations'][0]['intent']['slots']['INPUT_TEXT']['value']['originalValue']
    intent_name=intent_request['interpretations'][0]['intent']['name']
    sentimental_value=evaluate_openai(text_to_assess).lower()
    response_text=''
    if 'positive' in sentimental_value:
        response_text="I am glad to hear that you are happy!!"
    else:
        response_text="I am sorry to hear that you had a bad experience!!"


    output_session_attributes = {}
    return close(
        output_session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': response_text
        },
        intent_name,
        response_text
    )



def dispatch(intent_request):
    
    intent_name = intent_request['interpretations'][0]['intent']['name']
    if intent_name == 'GetSentiment':
        return evaluate_sentiment(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
