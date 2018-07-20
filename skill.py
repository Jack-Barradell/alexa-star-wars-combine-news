# Needed if want to use print
from __future__ import print_function
import feedparser
import re

FLASH_FEED = "http://www.swcombine.com/feeds/gns_flashnews.xml"
GNS_FEED = "http://www.swcombine.com/feeds/gns.xml"
SIM_FEED = "http://www.swcombine.com/feeds/news.xml"
DEFAULT_FLASH = 5
DEFAULT_GNS = 3
DEFAULT_SIM = 3


def generate_flash_response(session, count = DEFAULT_FLASH):
    session = {}
    title = "SWC News"

    flash_feed = feedparser.parse(FLASH_FEED)

    output = "Latest flash news. "

    for i,item in enumerate(flash_feed["items"]):
        if i == count:
            break

        title = re.sub('<[^<]+?>', '', item["title"])
        summary = re.sub('<[^<]+?>', '', item["summary"])

        output += "{}. ".format(title)
        output += "{}.. ".format(summary)

    reprompt = "reprompted template"
    end_session = False
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_help_response(session):
    session = {}
    title = "SWC News"
    output = "Some templated help"
    reprompt = "reprompted template"
    end_session = False
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_launch_response(session):
    session = {}
    title = "SWC News"
    output = "Welcome to swc news, would you like sim, g n s, or flash news?"
    reprompt = "Would you like sim, g n s, or flash news?"
    end_session = False
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_end_request(session):
    pass


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "AMAZON.HelpIntent":
        return generate_help_response(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return generate_end_request(session)
    elif intent_name == "flash":
        return generate_flash_response(session)
    else:
        raise ValueError("Invalid intent")


def on_ended(end_request, session):
    pass


def on_launch(launch_request, session):
    return generate_launch_response(session)


def generate_response(session_attributes, title, output, reprompt, end_session):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': {
            'outputSpeech': {
               'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
               'title': title,
               'content': output
            },
            'reprompt': {
                'outputSpeech': {
                   'type': 'PlainText',
                   'text': reprompt
              }
            },
            'shouldEndSession': end_session
        }
    }


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_ended(event['request'], event['session'])