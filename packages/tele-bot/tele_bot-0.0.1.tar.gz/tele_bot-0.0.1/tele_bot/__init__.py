import requests
import os


def send_message(text, token, group_id):
    os.environ['NO_PROXY'] = 'telegram.org'
    requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id=-{}&text={}'.format(token, group_id, text))
    print('message sent: ', text)
    
    
if __name__ == '__main__':
    send_message(text, token, group_id)