#codementor.py

import requests
import datetime
import time
import uuid
from pytz import timezone

cookies = {
    '_cacc':
    'b1b1c3ed5ab7b193012bd9be0ccbc9e4177cbae14c7f3303e7037c4469eb90b5df71b5204ec65de792c939af092845c151dd',
    '_lgn': '1',
}

headers = {
    'x-access-token':
    'b1b1c3ed5ab7b193012bd9be0ccbc9e4177cbae14c7f3303e7037c4469eb90b5df71b5204ec65de792c939af092845c151dd',
    'Accept': 'application/json, text/plain, */*',
    'x-requested-from': 'cm-mobile',
    # 'Cookie': '_cacc=b1b1c3ed5ab7b193012bd9be0ccbc9e4177cbae14c7f3303e7037c4469eb90b5df71b5204ec65de792c939af092845c151dd; _lgn=1',
    'Accept-Language': 'en-us',
    'User-Agent': 'Codementor/2 CFNetwork/1220.1 Darwin/20.3.0',
    'Connection': 'keep-alive',
}

from flask import Flask

app = Flask(__name)




def get_interested_sent_list():
  response_ = requests.get(
      'https://api.codementor.io/api/v2/requests/search?search_type=interested',
      cookies=cookies,
      headers=headers)
  response__ = requests.get(
      f"https://api.codementor.io/api/v2/requests/search?before_timestamp={response_.json()[14]['created_at']}&search_type=interested",
      cookies=cookies,
      headers=headers)
  response_1 = requests.get(
      f"https://api.codementor.io/api/v2/requests/search?before_timestamp={response__.json()[14]['created_at']}&search_type=interested",
      cookies=cookies,
      headers=headers)

  first_list = [i["random_key"] for i in response_.json()]
  # response_.json()[14]['created_at']
  first_list.extend([i["random_key"] for i in response__.json()])
  first_list.extend([i["random_key"] for i in response_1.json()])
  print("Intrested Fetched")
  return set(first_list)


def send_interest(random_key, user_name):

  json_data = {
      'message':
      f'''Hi {user_name},
After conducting a thorough investigation, we have determined that the root cause of the can be solved after a short discussion and guidance through a session. So, I propose the connect to solve the issues.
If you have any further questions, please do not hesitate to contact us.''',
  }
  print(
      f"Interest messgage sent to {user_name} at {str(datetime.datetime.now())}"
  )
  response = requests.post(
      f'https://api.codementor.io/api/v2/requests/{random_key}/interests',
      cookies=cookies,
      headers=headers,
      json=json_data,
  )
  return response.status_code


def send_message(user_name_id, user_name):
  json_data = {
      'message': {
          'content':
          f'Hi {user_name}, \nI am confident that I am the best candidate for your project. My extensive experience and skills in the field make me uniquely qualified to deliver exceptional results. I have a proven track record of successfully completing projects within budget and on time, while consistently exceeding client expectations. My attention to detail and ability to think outside the box ensure that I consistently deliver innovative solutions. In addition, I am a strong communicator and work well in collaborative environments. I am dedicated to building long-term relationships with clients and always strive to exceed their expectations. I would love the opportunity to discuss the project in more detail and show you why I am the best choice for your project. I look forward to hearing from you soon. Sincerely, Kshitiz',
          'type': 'message',
          'request': {
              'temp_message_id': str(uuid.uuid4()),
          },
      },
  }

  response = requests.post(
      f'https://api.codementor.io/api/v2/chats/messages/{user_name_id}',
      cookies=cookies,
      headers=headers,
      json=json_data,
  )
  print(f'Message sent to {user_name_id}')
  return response.status_code


# https://api.codementor.io/api/v2/requests/search?search_type=interested
sent_interested_list = get_interested_sent_list()


def main():

  response = requests.get(
      'https://api.codementor.io/api/v2/requests/search?search_type=all',
      cookies=cookies,
      headers=headers)
  notification_data = response.json()
  for i in range(notification_data.__len__()):
    # https://api.codementor.io/api/notifications/summary
    # latest_updatetime = 1699263813
    if notification_data[i]['random_key'] not in sent_interested_list:
      # latest_updatetime = notification_data[i]['created_at']
      random_key = notification_data[i].get('random_key')
      send_interest(random_key, notification_data[i]['user']['name'])
      time.sleep(5)
      send_message(notification_data[i]['user']['username'],
                   notification_data[i]['user']['name'])
      sent_interested_list.add(notification_data[i]['random_key'])

    else:
      print(f"Skipped {notification_data[i]['random_key']}",end = "")


# while True:
#   main()

# @app.route('/', methods=['GET'])
# def cron_endpoint():
#     main()
#     print(
#       f"rolled once {datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S.%f')}"
#   )
#     return "This is the /api/cron endpoint."

# if __name__ == '__main__':
#     app.run()


from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))
        print(f"rolled once {datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S.%f')}" )
        return main()
