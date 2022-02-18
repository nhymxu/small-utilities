import json
import urllib
from datetime import datetime


MONICA_API_URL = 'http://{{enter_here}}/api/reminders/upcoming/1'
MONICA_API_TOKEN = 'monica-api-token-here'

TELEGRAM_CHAT_ID = '{{enter_here}}'
TELEGRAM_BOT_TOKEN = '{{enter_here}}'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=HTML&disable_web_page_preview=true'

DAYS_START_NOTIFY = 3


def make_request(method="GET", url="", request_body=None):
    """
    Send API request ( json type )

    :param method:
    :param url:
    :param request_body:
    :return:
    """
    headers = {
        'Authorization': "Bearer {}".format(MONICA_API_TOKEN),
        'Content-Type': 'application/json'
    }

    data = None
    if request_body:
        # data = urllib.parse.urlencode(request_body)
        data = request_body.encode('ascii')

    try:
        req = urllib.request.Request(url, headers=headers, data=data, method=method)
        with urllib.request.urlopen(req) as response:
            resp_content = response.read()
            return resp_content
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
    except urllib.error.URLError as e:
        print(e.reason)

    return False


def send_telegram(message):
    """
    Send text message to Telegram using bot API

    :param message:
    :return:
    """
    text = urllib.parse.quote(message)
    url = f'{TELEGRAM_API_URL}&text={text}'

    raw_response = make_request(url=url)
    response = json.loads(raw_response)
    if not response['ok']:
        raise Exception("Failed to send message to Telegram")


def process_record(data):
    """
    Processing only recent reminders

    :param data:
    :return:
    """
    title = data['title']
    planned_date = datetime.strptime(data['planned_date'], '%Y-%m-%dT%H:%M:%S.000000Z')
    today = datetime.now()
    planned_date_str = planned_date.strftime("%d/%m/%Y")

    if abs((planned_date - today).days) > DAYS_START_NOTIFY:
        return

    msg = f"{title} - {planned_date_str}\n\n#notification"

    send_telegram(msg)


def run():
    """
    Main function to handle upcoming event

    :return:
    """
    response = make_request(url=MONICA_API_URL)
    response_json = json.loads(response)

    reminders = response_json.get('data')

    for record in reminders:
        process_record(record)


if __name__ == "__main__":
    run()
