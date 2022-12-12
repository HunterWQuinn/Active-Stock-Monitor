
import requests
import json
from twilio.rest import Client

class StockWatcher():
    '''
    This class reads the config json and notifies users based on stock prices
    '''
    def __init__(self):
        with open('secret.py') as api_keys:
            keys = json.load(api_keys)
            rapid_api_key = keys['rapid_key']
            twilio_api_key = keys['twilio_key']

        # pull stocks from json
        with open('config.json') as json_file:
            data = json.load(json_file)
            send_text: bool = data['text']
            phone = data['phone']
            base_message = data["message"]
            stock_data = data['stock_data']

        # parse out the price point

        all_stocks = stock_data.keys()
        for stock in all_stocks:
            selling_point = stock_data[stock]['notify at']

            # pull api data
            url = f"https://realstonks.p.rapidapi.com/{stock}"

            headers = {
                "X-RapidAPI-Key": f"{rapid_api_key}",
                "X-RapidAPI-Host": "realstonks.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers)

            json_split = (response.text).split(',')
            json_split = json_split[0].split(' ')
            current_value = float(json_split[1])
            print(f'{stock}: {current_value}')
            if current_value > selling_point:
                message = f'{base_message}  Stock: {stock}, Current Price: {current_value}, Set at: {selling_point}'
                if send_text:
                    self.text_message(message=message, to=phone, twilio_api_key=twilio_api_key)


    def text_message(self, message: str, to: str, twilio_api_key: str):
        account_sid = 'AC4efad21d87028bcb7a1dcf70d8696835'
        auth_token = f'{twilio_api_key}'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            messaging_service_sid='MGda1fc98490c5d896df7bd4549a2cf1be',
            body=message,
            to=f'+1{to}'
        )
        print('Text Message sent!')

def main():
    print('Running Stock Watcher by Hunter Quinn')
    StockWatcher()

main()