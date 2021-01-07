import os
import requests
import string

LIVEBOT_HOST = os.environ.get('BOT_SERVER_HOST', 'localhost')
LIVEPOT_PORT = os.environ.get('BOT_SERVER_PORT', 10555)
LIVEBOT_URL = f'http://{LIVEBOT_HOST}:{LIVEPOT_PORT}/livebots'
LIVEBOT_DELETE_URL_TEMPLATE = string.Template(f'http://{LIVEBOT_HOST}:{LIVEPOT_PORT}/livebot/$bot_id')

def convert_form_to_bot_request(form_data):
    source = form_data['source']
    analysis_type = form_data['analysis_type']

    if analysis_type == 'live':
        url = LIVEBOT_URL
    else:
        raise NotImplementedError(f"Analysis Type {analysis_type} not supported")
    analyzer = form_data['analyzer']
    query = form_data['query']

    POST_request = {'source':source, 'analyzer_settings':analyzer, 'query':query}
    return url, POST_request

def request_new_bot(url, POST_request):
    response = requests.post(url, POST_request)
    return response

def delete_bot(bot_id):
    url = LIVEBOT_DELETE_URL_TEMPLATE.substitute(bot_id=bot_id)
    return requests.delete(url)


def get_botlist():
    return requests.get(LIVEBOT_URL)
