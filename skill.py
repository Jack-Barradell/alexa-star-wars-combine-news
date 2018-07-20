# Needed if want to use print
from __future__ import print_function


def generate_help_response(session):
    session = {}
    title = "Needs help"
    output = "Some templated help"
    reprompt = "reprompted template"
    end_session = False
    response = generate_response(session, title, output, reprompt, end_session)
    return response


def generate_launch_response(session):
    session = {}
    title = "Test Title"
    output = "Welcome to the template"
    reprompt = "Did you hear? You are in the template"
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