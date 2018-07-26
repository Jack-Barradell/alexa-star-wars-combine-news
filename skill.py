# Needed if want to use print
from __future__ import print_function
import feedparser
import re

# Sources for news
FLASH_FEED = "http://www.swcombine.com/feeds/gns_flashnews.xml"
GNS_FEED = "http://www.swcombine.com/feeds/gns.xml"
SIM_FEED = "http://www.swcombine.com/feeds/news.xml"

# Default news to pull
DEFAULT_FLASH = 5
DEFAULT_GNS = 3
DEFAULT_SIM = 3


def generate_sim_title_response(session, count = DEFAULT_SIM):
    session = {}
    title = "SWC News"
    output = "Latest sim news, starting with the newest. \n"

    sim_feed = feedparser.parse(SIM_FEED)

    # Verifies there is some news
    if sim_feed.get("items"):
        for i,item in enumerate(sim_feed["items"]):

            # Limits the number of news items presented
            if i == count:
                break

            # Strip any tags from the title
            item_title = re.sub('<[^<]+?>', '', item["title"])

            # Builds the response
            output += "{}. ".format(item_title)
            output += "posted by {}. ".format(item["author"])
            output += ". . . \n"

    else:
        output += "Sorry, no sim news available... "

    reprompt = "Would you like sim, g n s, or flash news?"
    end_session = True
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_gns_title_response(session, count = DEFAULT_GNS):
    session = {}
    title = "SWC News"
    output = "Latest g n s news, starting with the newest. \n"

    gns_feed = feedparser.parse(GNS_FEED)

    # Verifies there is actually some news
    if gns_feed.get("items"):
        for i,item in enumerate(gns_feed["items"]):

            # Limits the number of items fed
            if i == count:
                break

            # Strips any tags fro the title
            item_title = re.sub('<[^<]+?>', '', item["title"])

            # Builds tthe response
            output += "{}. ".format(item_title)
            output += " published by {}. ".format(item["author"])
            output += " on behalf of {}. . . \n".format(item["faction"])

    else:
        output += "Sorry, no g n s news available... "

    reprompt = "Would you like sim, g n s, or flash news?"
    end_session = True
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_flash_response(session, count = DEFAULT_FLASH):
    session = {}
    title = "SWC News"

    flash_feed = feedparser.parse(FLASH_FEED)

    output = "Latest flash news, starting with the newest. \n"

    # Verifies theres is actually some news
    if flash_feed.get("items"):
        for i,item in enumerate(flash_feed["items"]):

            # Limits the number of items 
            if i == count:
                break

            # Strips any tags from the news and title
            item_title = re.sub('<[^<]+?>', '', item["title"])
            summary = re.sub('<[^<]+?>', '', item["summary"])

            output += "{}. ".format(item_title)

            # Blocks certain flash news where the title and content are the same
            if not item_title == summary:
                output += "{}".format(summary)

            output += ". . . \n"

    else:
        output += "Sorry, no flash news available..."

    reprompt = "Would you like sim, g n s, or flash news?"
    end_session = True
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_help_response(session):
    session = {}
    title = "SWC News"
    output = "Ask me for the latest sim, g n s or flash news!"
    reprompt = "Would you like sim, g n s, or flash news?"
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
    session = {}
    title = "SWC News"
    output = "Goodbye"
    reprompt = "Goodbye"
    end_session = True
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Routes the intents, splitting on intents where there can be a slotted number
    if intent_name == "AMAZON.HelpIntent" or intent_name == "AMAZON.FallbackIntent":
        return generate_help_response(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return generate_end_request(session)
    elif intent_name == "flash":
        if intent['slots']['number'].get('value'):
            return generate_flash_response(session, int(intent['slots']['number'].get('value')))
        else:
            return generate_flash_response(session)
    elif intent_name == "gns":
        if intent['slots']['number'].get('value'):
            return generate_gns_title_response(session, int(intent['slots']['number'].get('value')))
        else:
            return generate_gns_title_response(session)
    elif intent_name == 'sim':
        if intent['slots']['number'].get('value'):
            return generate_sim_title_response(session, int(intent['slots']['number'].get('value')))
        else:
            return generate_sim_title_response(session) 
    else:
        return generate_help_response(session)


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