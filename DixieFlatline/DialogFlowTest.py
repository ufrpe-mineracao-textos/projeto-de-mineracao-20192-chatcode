import dialogflow
import os
from google.api_core.exceptions import InvalidArgument
from google.cloud import storage

storage_client = storage.Client()

DIALOGFLOW_PROJECT_ID = 'small-talk-bbkibx'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'small-talk-bbkibx-ea8cfaa45069.json'
SESSION_ID = 'current-user-id'

text_to_be_analyzed = "Hello"

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)

try:
    response = storage_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise